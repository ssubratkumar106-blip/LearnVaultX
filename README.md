# LearnVaultX - AI-Based Virtual Teaching Platform

A web-based educational platform with AI-powered features, offline support, and adaptive learning analytics for institutes and students.

## Features

- **Role-Based System**: Separate dashboards for teachers and students
- **Content Management**: Teachers can create classes, upload lectures (PDF/video), and create quizzes
- **AI Chatbot**: Intelligent assistant for student queries powered by Groq AI
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

2. Create `.env` file (optional for AI features):
```env
GROQ_API_KEY=your_groq_api_key_here
```

3. Run the application:
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

## Troubleshooting

**Port in use?** Change port in `app.py`:
```python
socketio.run(app, port=8000)
```

**Database issues?** Reset database:
```bash
rm education.db
python -c "from app import init_db; init_db()"
```

## License

Educational project - free to use and modify.

---

Built for BPUT Hackathon Mid-Evaluation
