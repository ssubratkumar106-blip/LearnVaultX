// Main JavaScript for LearnVaultX Platform

// Register Service Worker for offline support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then(registration => {
                console.log('Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// AI Chatbot functionality
let aiPanelOpen = false;

function toggleAIPanel() {
    const panel = document.getElementById('ai-chatbot');
    aiPanelOpen = !aiPanelOpen;
    
    if (aiPanelOpen) {
        panel.classList.remove('hidden');
    } else {
        panel.classList.add('hidden');
    }
}

async function sendAIMessage() {
    const input = document.getElementById('ai-input');
    const prompt = input.value.trim();
    
    if (!prompt) return;
    
    const messagesContainer = document.getElementById('ai-messages');
    
    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'ai-message user';
    userMessage.innerHTML = `<p>${escapeHtml(prompt)}</p>`;
    messagesContainer.appendChild(userMessage);
    
    // Clear input
    input.value = '';
    
    // Add loading message
    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'ai-message loading';
    loadingMessage.id = 'ai-loading';
    loadingMessage.innerHTML = '<p>Thinking...</p>';
    messagesContainer.appendChild(loadingMessage);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    try {
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });
        
        const data = await response.json();
        
        // Remove loading message
        document.getElementById('ai-loading').remove();
        
        // Add AI response (rendered HTML from backend includes markdown and math)
        const aiMessage = document.createElement('div');
        aiMessage.className = 'ai-message bot';
        // Don't escape HTML since backend returns rendered markdown
        aiMessage.innerHTML = `<div class="ai-content">${data.answer}</div>`;
        messagesContainer.appendChild(aiMessage);
        
        // Trigger MathJax rendering for math equations
        if (typeof MathJax !== 'undefined' && MathJax.typeset) {
            MathJax.typeset([aiMessage]);
        }
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
    } catch (error) {
        console.error('Error sending message to AI:', error);
        
        // Remove loading message
        const loading = document.getElementById('ai-loading');
        if (loading) loading.remove();
        
        // Add error message
        const errorMessage = document.createElement('div');
        errorMessage.className = 'ai-message bot';
        errorMessage.innerHTML = '<p>Sorry, I encountered an error. Please try again.</p>';
        messagesContainer.appendChild(errorMessage);
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Handle Enter key in AI input
document.addEventListener('DOMContentLoaded', () => {
    const aiInput = document.getElementById('ai-input');
    if (aiInput) {
        aiInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendAIMessage();
            }
        });
    }
});

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// IndexedDB for offline storage
const DB_NAME = 'learnvaultx-offline';
const DB_VERSION = 1;
let db;

function initIndexedDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => {
            db = request.result;
            resolve(db);
        };
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            
            // Create object stores
            if (!db.objectStoreNames.contains('lectures')) {
                db.createObjectStore('lectures', { keyPath: 'id' });
            }
            
            if (!db.objectStoreNames.contains('quizzes')) {
                db.createObjectStore('quizzes', { keyPath: 'id' });
            }
            
            if (!db.objectStoreNames.contains('offline-queue')) {
                db.createObjectStore('offline-queue', { autoIncrement: true });
            }
        };
    });
}

// Save data for offline access
async function saveForOffline(storeName, data) {
    if (!db) await initIndexedDB();
    
    return new Promise((resolve, reject) => {
        const transaction = db.transaction([storeName], 'readwrite');
        const store = transaction.objectStore(storeName);
        const request = store.put(data);
        
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Get offline data
async function getOfflineData(storeName, id) {
    if (!db) await initIndexedDB();
    
    return new Promise((resolve, reject) => {
        const transaction = db.transaction([storeName], 'readonly');
        const store = transaction.objectStore(storeName);
        const request = id ? store.get(id) : store.getAll();
        
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Queue action for when back online
async function queueOfflineAction(action) {
    if (!db) await initIndexedDB();
    
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['offline-queue'], 'readwrite');
        const store = transaction.objectStore('offline-queue');
        const request = store.add(action);
        
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Process offline queue when back online
async function processOfflineQueue() {
    if (!db) await initIndexedDB();
    
    const transaction = db.transaction(['offline-queue'], 'readonly');
    const store = transaction.objectStore('offline-queue');
    const request = store.getAll();
    
    request.onsuccess = async () => {
        const actions = request.result;
        
        for (const action of actions) {
            try {
                // Process action based on type
                if (action.type === 'quiz-submission') {
                    await fetch('/api/submit_quiz', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(action.data)
                    });
                }
                // Add more action types as needed
                
                // Remove from queue
                const deleteTransaction = db.transaction(['offline-queue'], 'readwrite');
                const deleteStore = deleteTransaction.objectStore('offline-queue');
                deleteStore.delete(action.id);
            } catch (error) {
                console.error('Error processing offline action:', error);
            }
        }
    };
}

// Check online status
window.addEventListener('online', () => {
    console.log('Back online! Processing offline queue...');
    processOfflineQueue();
    
    // Show notification
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Back Online', {
            body: 'Syncing your offline activities...',
            icon: '/static/icon.png'
        });
    }
});

window.addEventListener('offline', () => {
    console.log('You are offline. Data will be saved locally.');
    
    // Show notification
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Offline Mode', {
            body: 'You can continue working. Changes will sync when online.',
            icon: '/static/icon.png'
        });
    }
});

// Request notification permission
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Download lecture for offline access
async function downloadLectureForOffline(lectureId, lectureData) {
    try {
        await saveForOffline('lectures', {
            id: lectureId,
            ...lectureData,
            downloadedAt: new Date().toISOString()
        });
        
        alert('Lecture saved for offline access!');
    } catch (error) {
        console.error('Error saving lecture:', error);
        alert('Failed to save lecture for offline access.');
    }
}

// Cache quiz for offline access
async function cacheQuizForOffline(quizId, quizData) {
    try {
        await saveForOffline('quizzes', {
            id: quizId,
            ...quizData,
            cachedAt: new Date().toISOString()
        });
        
        console.log('Quiz cached for offline access');
    } catch (error) {
        console.error('Error caching quiz:', error);
    }
}

// Initialize IndexedDB when page loads
initIndexedDB().catch(console.error);

// Utility: Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Utility: Format time
function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ===========================================================================
// NEW FEATURES: Feedback, Live Class, Chat Fixes, Sidebar Toggle, Speed Test
// ===========================================================================

// Sidebar Toggle Functionality
let sidebarOpen = true;

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const toggleBtn = document.querySelector('.sidebar-toggle');
    
    if (!sidebar) return;
    
    sidebarOpen = !sidebarOpen;
    
    if (sidebarOpen) {
        sidebar.classList.remove('collapsed');
        if (mainContent) mainContent.classList.remove('expanded');
        if (toggleBtn) toggleBtn.innerHTML = '☰';
    } else {
        sidebar.classList.add('collapsed');
        if (mainContent) mainContent.classList.add('expanded');
        if (toggleBtn) toggleBtn.innerHTML = '☰';
    }
    
    // Save state to localStorage
    localStorage.setItem('sidebarOpen', sidebarOpen);
}

// Restore sidebar state on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedState = localStorage.getItem('sidebarOpen');
    if (savedState !== null && savedState === 'false') {
        toggleSidebar();
    }
});

// Feedback Modal Functions
function openFeedbackModal() {
    const modal = document.getElementById('feedback-modal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeFeedbackModal() {
    const modal = document.getElementById('feedback-modal');
    if (modal) {
        modal.style.display = 'none';
        // Reset form
        document.getElementById('feedback-form').reset();
        const stars = document.querySelectorAll('.star');
        stars.forEach(star => star.classList.remove('active'));
    }
}

let selectedRating = 0;

function selectRating(rating) {
    selectedRating = rating;
    const stars = document.querySelectorAll('.star');
    
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

async function submitFeedback() {
    if (selectedRating === 0) {
        alert('Please select a rating');
        return;
    }
    
    const message = document.getElementById('feedback-message').value.trim();
    const submitBtn = document.querySelector('#feedback-form button[type="button"]');
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rating: selectedRating,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(data.message || 'Thank you for your feedback!');
            closeFeedbackModal();
        } else {
            alert(data.error || 'Failed to submit feedback');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Feedback';
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        alert('Network error. Please try again.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Feedback';
    }
}

// Live Class Functions (Jitsi Integration)
let activeJitsiMeeting = null;

async function startLiveClass(classId) {
    try {
        const response = await fetch('/api/live-class/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ class_id: classId })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            openJitsiMeeting(data.room_name, data.jitsi_domain, classId);
        } else {
            alert(data.error || 'Failed to start live class');
        }
    } catch (error) {
        console.error('Error starting live class:', error);
        alert('Failed to start live class');
    }
}

async function joinLiveClass(classId) {
    try {
        const response = await fetch(`/api/live-class/join/${classId}`);
        const data = await response.json();
        
        if (response.ok) {
            openJitsiMeeting(data.room_name, data.jitsi_domain, classId);
        } else {
            alert(data.error || 'No active live session');
        }
    } catch (error) {
        console.error('Error joining live class:', error);
        alert('Failed to join live class');
    }
}

function openJitsiMeeting(roomName, jitsiDomain, classId) {
    // Create modal for Jitsi
    const modal = document.createElement('div');
    modal.id = 'jitsi-modal';
    modal.className = 'jitsi-modal';
    modal.innerHTML = `
        <div class="jitsi-container">
            <div class="jitsi-header">
                <h3>Live Class</h3>
                <div id="speed-indicator" class="speed-indicator">
                    <span class="speed-dot"></span>
                    <span class="speed-text">Checking...</span>
                </div>
                <button class="close-jitsi-btn" onclick="closeLiveClass(${classId})">✕ End Class</button>
            </div>
            <div id="jitsi-meet" style="height: calc(100vh - 60px);"></div>
        </div>
    `;
    document.body.appendChild(modal);
    
    // Load Jitsi API if not already loaded
    if (typeof JitsiMeetExternalAPI === 'undefined') {
        const script = document.createElement('script');
        script.src = `https://${jitsiDomain}/external_api.js`;
        script.onload = () => initializeJitsi(roomName, jitsiDomain);
        document.head.appendChild(script);
    } else {
        initializeJitsi(roomName, jitsiDomain);
    }
    
    // Start speed indicator
    startSpeedIndicator();
}

function initializeJitsi(roomName, jitsiDomain) {
    const domain = jitsiDomain;
    const options = {
        roomName: roomName,
        width: '100%',
        height: '100%',
        parentNode: document.getElementById('jitsi-meet'),
        configOverwrite: {
            prejoinPageEnabled: false,
            startWithAudioMuted: false,
            startWithVideoMuted: false
        },
        interfaceConfigOverwrite: {
            TOOLBAR_BUTTONS: [
                'microphone', 'camera', 'closedcaptions', 'desktop', 'fullscreen',
                'fodeviceselection', 'hangup', 'profile', 'chat', 'recording',
                'livestreaming', 'etherpad', 'sharedvideo', 'settings', 'raisehand',
                'videoquality', 'filmstrip', 'invite', 'feedback', 'stats', 'shortcuts',
                'tileview', 'videobackgroundblur', 'download', 'help', 'mute-everyone'
            ]
        }
    };
    
    activeJitsiMeeting = new JitsiMeetExternalAPI(domain, options);
}

async function closeLiveClass(classId) {
    if (confirm('Are you sure you want to end the live class?')) {
        // Close Jitsi
        if (activeJitsiMeeting) {
            activeJitsiMeeting.dispose();
            activeJitsiMeeting = null;
        }
        
        // Remove modal
        const modal = document.getElementById('jitsi-modal');
        if (modal) modal.remove();
        
        // Stop speed indicator
        stopSpeedIndicator();
        
        // Notify server
        try {
            await fetch('/api/live-class/end', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ class_id: classId })
            });
        } catch (error) {
            console.error('Error ending live class:', error);
        }
    }
}

// Internet Speed Indicator
let speedTestInterval = null;
let globalSpeedIndicatorActive = false;

async function testInternetSpeed() {
    const startTime = performance.now();
    // Use a small image from a reliable CDN
    const imageUrl = 'https://www.google.com/images/phd/px.gif?' + Math.random();
    const downloadSize = 5000; // approximate size in bytes
    
    try {
        const response = await fetch(imageUrl, { 
            cache: 'no-store',
            mode: 'no-cors' // Avoid CORS issues
        });
        const endTime = performance.now();
        const duration = (endTime - startTime) / 1000; // in seconds
        const bitsLoaded = downloadSize * 8;
        const speedBps = bitsLoaded / duration;
        const speedMbps = (speedBps / (1024 * 1024)).toFixed(2);
        
        return parseFloat(speedMbps);
    } catch (error) {
        console.error('Speed test error:', error);
        return 0;
    }
}

function updateGlobalSpeedIndicator(speed) {
    const valueElement = document.getElementById('speed-value');
    const statusDot = document.querySelector('.speed-status .speed-dot');
    
    if (!valueElement || !statusDot) return;
    
    // Remove existing classes
    statusDot.classList.remove('good', 'fair', 'poor');
    
    if (speed > 2) {
        statusDot.classList.add('good');
        valueElement.textContent = `${speed} Mbps`;
    } else if (speed > 0.5) {
        statusDot.classList.add('fair');
        valueElement.textContent = `${speed} Mbps`;
    } else if (speed > 0) {
        statusDot.classList.add('poor');
        valueElement.textContent = `${speed} Mbps`;
    } else {
        valueElement.textContent = 'Offline';
        statusDot.classList.add('poor');
    }
}

function updateSpeedIndicator(speed) {
    // For Jitsi modal
    const indicator = document.getElementById('speed-indicator');
    if (indicator) {
        const dot = indicator.querySelector('.speed-dot');
        const text = indicator.querySelector('.speed-text');
        
        if (dot && text) {
            if (speed > 2) {
                dot.style.backgroundColor = '#4caf50'; // green
                text.textContent = `${speed} Mbps - Good`;
            } else if (speed > 0.5) {
                dot.style.backgroundColor = '#ff9800'; // orange
                text.textContent = `${speed} Mbps - Fair`;
            } else {
                dot.style.backgroundColor = '#f44336'; // red
                text.textContent = `${speed} Mbps - Poor`;
            }
        }
    }
}

function startGlobalSpeedIndicator() {
    if (globalSpeedIndicatorActive) return;
    
    globalSpeedIndicatorActive = true;
    
    // Test immediately
    testInternetSpeed().then(updateGlobalSpeedIndicator);
    
    // Test every 15 seconds
    speedTestInterval = setInterval(async () => {
        const speed = await testInternetSpeed();
        updateGlobalSpeedIndicator(speed);
    }, 15000);
}

function startSpeedIndicator() {
    // Test immediately
    testInternetSpeed().then(updateSpeedIndicator);
    
    // Test every 10 seconds
    if (!speedTestInterval) {
        speedTestInterval = setInterval(async () => {
            const speed = await testInternetSpeed();
            updateSpeedIndicator(speed);
        }, 10000);
    }
}

function stopSpeedIndicator() {
    if (speedTestInterval) {
        clearInterval(speedTestInterval);
        speedTestInterval = null;
    }
}

// Make network speed indicator draggable
function makeDraggable(element) {
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    // Load saved position from localStorage
    const savedPosition = localStorage.getItem('speedIndicatorPosition');
    if (savedPosition) {
        const { x, y } = JSON.parse(savedPosition);
        xOffset = x;
        yOffset = y;
        setPosition(x, y);
    }

    // Mouse events
    element.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    // Touch events for mobile
    element.addEventListener('touchstart', dragStart, { passive: false });
    document.addEventListener('touchmove', drag, { passive: false });
    document.addEventListener('touchend', dragEnd);

    function dragStart(e) {
        // Only drag if clicking on the indicator itself, not on links/buttons inside
        if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
            return;
        }

        if (e.type === 'touchstart') {
            initialX = e.touches[0].clientX - xOffset;
            initialY = e.touches[0].clientY - yOffset;
        } else {
            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;
        }

        isDragging = true;
        element.style.cursor = 'grabbing';
        e.preventDefault();
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();

            if (e.type === 'touchmove') {
                currentX = e.touches[0].clientX - initialX;
                currentY = e.touches[0].clientY - initialY;
            } else {
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
            }

            xOffset = currentX;
            yOffset = currentY;

            setPosition(currentX, currentY);
        }
    }

    function dragEnd(e) {
        if (isDragging) {
            // Save position to localStorage
            localStorage.setItem('speedIndicatorPosition', JSON.stringify({
                x: xOffset,
                y: yOffset
            }));

            isDragging = false;
            element.style.cursor = 'grab';
        }
    }

    function setPosition(x, y) {
        // Ensure the indicator stays within viewport bounds
        const rect = element.getBoundingClientRect();
        const maxX = window.innerWidth - rect.width;
        const maxY = window.innerHeight - rect.height;

        x = Math.max(0, Math.min(x, maxX));
        y = Math.max(0, Math.min(y, maxY));

        element.style.position = 'fixed';
        element.style.left = `${x}px`;
        element.style.top = `${y}px`;
        element.style.right = 'auto';
        element.style.bottom = 'auto';
    }

    // Add visual hint that it's draggable
    element.style.cursor = 'grab';
    element.title = 'Drag to move';
}

// Reset indicator position (double-click to reset to default)
function resetIndicatorPosition() {
    const indicator = document.getElementById('network-speed-indicator');
    if (indicator) {
        localStorage.removeItem('speedIndicatorPosition');
        indicator.style.position = '';
        indicator.style.left = '';
        indicator.style.top = '';
        indicator.style.right = '';
        indicator.style.bottom = '';
        alert('Network indicator position reset to default!');
    }
}

// Initialize global speed indicator on page load
document.addEventListener('DOMContentLoaded', () => {
    const indicator = document.getElementById('network-speed-indicator');
    if (indicator) {
        startGlobalSpeedIndicator();
        makeDraggable(indicator);
        
        // Double-click to reset position
        indicator.addEventListener('dblclick', (e) => {
            e.preventDefault();
            resetIndicatorPosition();
        });
    }
});

// Chat Box Auto-Scroll Fix
function scrollChatToBottom() {
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Auto-scroll chat when new message arrives (use MutationObserver)
document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
        const observer = new MutationObserver(() => {
            scrollChatToBottom();
        });
        
        observer.observe(chatMessages, {
            childList: true,
            subtree: true
        });
    }
});

// Export functions for use in other scripts
window.LearnVaultX = {
    toggleAIPanel,
    sendAIMessage,
    saveForOffline,
    getOfflineData,
    queueOfflineAction,
    downloadLectureForOffline,
    cacheQuizForOffline,
    formatDate,
    formatTime,
    // New features
    toggleSidebar,
    openFeedbackModal,
    closeFeedbackModal,
    selectRating,
    submitFeedback,
    startLiveClass,
    joinLiveClass,
    closeLiveClass,
    scrollChatToBottom
};

