# LearnVaultX - AI-Based Virtual Teaching Platform

A web-based educational platform with AI-powered features, offline support, and adaptive learning analytics for institutes and students.

## Features

### **🤖 AI-Driven Adaptive Learning (NEW!)**
- **Knowledge Gap Detection**: AI analyzes quiz performance to identify weak topics
- **Personalized Recommendations**: AI suggests specific lectures/quizzes based on gaps
- **Context-Aware AI Tutor**: Chatbot knows student performance and provides personalized help
- **Teacher Intervention Alerts**: Automated alerts for struggling students
- **Topic Mastery Tracking**: Visual breakdown of mastery levels per topic

### **Core Features**
- **Role-Based System**: Separate dashboards for teachers and students
- **Content Management**: Teachers can create classes, upload lectures (PDF/video), and create quizzes
- **AI Chatbot**: Powered by Claude 4.5 Sonnet (or Groq/DeepSeek fallback)
- **Real-Time Chat**: Live class discussions using WebSockets
- **Offline Support**: Service Worker and IndexedDB for rural connectivity
- **Analytics Dashboard**: Track student performance and learning pace
- **Responsive Design**: Works on desktop, tablet, and mobile

## Tech Stack

**Backend**: Flask, Flask-SocketIO, SQLite  
**Frontend**: HTML5, CSS3, Vanilla JavaScript  
**AI Integration**: Groq API (LLaMA 3.1)  
**PWA**: Service Workers, IndexedDB

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file for AI features:
```env
# Claude AI (Recommended - Best for education!)
ANTHROPIC_API_KEY=your_claude_api_key_here

# OR use Groq (FREE & Fast alternative)
GROQ_API_KEY=your_groq_api_key_here

# Flask
FLASK_SECRET_KEY=your-secret-key-here
```

**Get Claude API Key (FREE $5 credits!):**
- Visit: https://console.anthropic.com/
- Sign up → Get API key → Add to `.env`
- See `ADAPTIVE_LEARNING_GUIDE.md` for details

3. Initialize database and load demo data:
```bash
python -c "from app import init_db; init_db()"
python seed_data.py
```

4. Run the application:
```bash
python app.py
```

Access at: `http://localhost:5000`

### Load Demo Data

```bash
python seed_data.py
```

Demo accounts:
- Teachers: `teacher1@edu.com`, `teacher2@edu.com`
- Students: `student1@edu.com` to `student5@edu.com`
- Password: `password123`

## Usage

### Teachers
1. Create and manage classes
2. Upload lecture materials
3. Create quizzes with multiple-choice questions
4. View student analytics and performance

### Students
1. Join available classes
2. Access and download lectures
3. Take quizzes
4. Use AI chatbot for help
5. Participate in class discussions

## Project Structure

```
Project/
├── app.py              # Main Flask application
├── schema.sql          # Database schema
├── seed_data.py        # Demo data loader
├── templates/          # HTML templates
├── static/
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── uploads/        # User uploaded files
└── education.db        # SQLite database
```

## Learning Pace Algorithm

```
pace_score = 10 × (0.5×accuracy + 0.3×speed + 0.2×engagement)
```

- **Accuracy**: Quiz scores
- **Speed**: Completion time
- **Engagement**: Chat participation

## Security

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- Secure file uploads with validation

## Offline Mode

- Service Worker caches static assets and lectures
- IndexedDB stores quizzes locally
- Automatic sync when connection restored

## 🆕 Adaptive Learning Features

### **For Students:**
- **📚 AI Recommendations Tab**: Personalized content suggestions based on your gaps
- **🎯 Knowledge Gaps Tab**: Visual breakdown of topic mastery levels
- **🤖 Context-Aware AI**: Chatbot knows your performance and helps accordingly

### **For Teachers:**
- **🚨 Student Alerts Tab**: Automated intervention alerts for struggling students
- **📊 Enhanced Analytics**: Topic-wise mastery tracking for all students
- **⚡ Proactive Monitoring**: AI detects issues automatically, no manual checking

### **Documentation:**
- `ADAPTIVE_LEARNING_GUIDE.md` - Complete guide to adaptive features
- `SETUP_ADAPTIVE_FEATURES.md` - Quick 5-minute setup
- `CHANGES_SUMMARY.md` - Detailed change log

## Troubleshooting

**Port in use?** Change port in `app.py`:
```python
socketio.run(app, port=8000)
```

**Database issues?** Reset database:
```bash
rm education.db
python -c "from app import init_db; init_db()"
python seed_data.py  # Important: Loads topics for adaptive features!
```

**AI not working?** Check your API key in `.env`:
```bash
cat .env | grep ANTHROPIC  # Should show your key
python app.py  # Look for "Claude AI initialized" in logs
```

**No recommendations showing?** Make sure topics are loaded:
```bash
python seed_data.py  # Creates topics and assigns to questions
```

## License

Educational project - free to use and modify.

---

Built for BPUT Hackathon Mid-Evaluation | Enhanced with AI-Driven Adaptive Learning
