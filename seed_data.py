"""
Seed script to populate database with demo data for testing and hackathon demo
"""

import sqlite3
import json
from werkzeug.security import generate_password_hash

def seed_database():
    # Connect to database
    db = sqlite3.connect('education.db')
    cursor = db.cursor()
    
    print("🌱 Seeding database with demo data...")
    
    # Create users (teachers and students)
    print("Creating users...")
    
    users = [
        # Teachers
        ('Dr. Sarah Johnson', 'teacher1@edu.com', 'password123', 'teacher'),
        ('Prof. Michael Chen', 'teacher2@edu.com', 'password123', 'teacher'),
        
        # Students
        ('Alice Smith', 'student1@edu.com', 'password123', 'student'),
        ('Bob Wilson', 'student2@edu.com', 'password123', 'student'),
        ('Charlie Brown', 'student3@edu.com', 'password123', 'student'),
        ('Diana Prince', 'student4@edu.com', 'password123', 'student'),
        ('Ethan Hunt', 'student5@edu.com', 'password123', 'student'),
    ]
    
    for name, email, password, role in users:
        password_hash = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
            (name, email, password_hash, role)
        )
    
    db.commit()
    print(f"✅ Created {len(users)} users")
    
    # Create classes
    print("Creating classes...")
    
    classes = [
        (1, 'Data Structures and Algorithms', 'Learn fundamental data structures and algorithms for efficient problem solving'),
        (1, 'Web Development Fundamentals', 'Master HTML, CSS, JavaScript and modern web development'),
        (2, 'Artificial Intelligence', 'Introduction to AI, machine learning, and neural networks'),
    ]
    
    for teacher_id, title, description in classes:
        cursor.execute(
            'INSERT INTO classes (teacher_id, title, description) VALUES (?, ?, ?)',
            (teacher_id, title, description)
        )
    
    db.commit()
    print(f"✅ Created {len(classes)} classes")
    
    # Enroll students in classes
    print("Enrolling students...")
    
    enrollments = [
        (3, 1), (3, 2),  # Alice in DSA and Web Dev
        (4, 1), (4, 3),  # Bob in DSA and AI
        (5, 1), (5, 2), (5, 3),  # Charlie in all classes
        (6, 2), (6, 3),  # Diana in Web Dev and AI
        (7, 1),  # Ethan in DSA
    ]
    
    for student_id, class_id in enrollments:
        cursor.execute(
            'INSERT INTO enrollments (student_id, class_id) VALUES (?, ?)',
            (student_id, class_id)
        )
    
    db.commit()
    print(f"✅ Created {len(enrollments)} enrollments")
    
    # Create some sample lectures (file paths would be actual uploaded files in production)
    print("Creating sample lectures...")
    
    lectures = [
        (1, 'arrays_and_linked_lists.pdf', 'static/uploads/arrays_and_linked_lists.pdf'),
        (1, 'trees_and_graphs.pdf', 'static/uploads/trees_and_graphs.pdf'),
        (2, 'html_css_basics.pdf', 'static/uploads/html_css_basics.pdf'),
        (2, 'javascript_fundamentals.pdf', 'static/uploads/javascript_fundamentals.pdf'),
        (3, 'intro_to_ml.pdf', 'static/uploads/intro_to_ml.pdf'),
    ]
    
    for class_id, filename, filepath in lectures:
        cursor.execute(
            'INSERT INTO lectures (class_id, filename, filepath) VALUES (?, ?, ?)',
            (class_id, filename, filepath)
        )
    
    db.commit()
    print(f"✅ Created {len(lectures)} lectures")
    
    # Create quizzes
    print("Creating quizzes...")
    
    quizzes = [
        (1, 'Arrays and Linked Lists Quiz'),
        (1, 'Binary Trees Assessment'),
        (2, 'HTML & CSS Quiz'),
        (3, 'Machine Learning Basics'),
    ]
    
    for class_id, title in quizzes:
        cursor.execute(
            'INSERT INTO quizzes (class_id, title) VALUES (?, ?)',
            (class_id, title)
        )
    
    db.commit()
    print(f"✅ Created {len(quizzes)} quizzes")
    
    # Create quiz questions
    print("Creating quiz questions...")
    
    # Quiz 1: Arrays and Linked Lists
    quiz_1_questions = [
        {
            'quiz_id': 1,
            'question': 'What is the time complexity of accessing an element in an array by index?',
            'options': ['O(1)', 'O(n)', 'O(log n)', 'O(n^2)'],
            'correct': 0
        },
        {
            'quiz_id': 1,
            'question': 'Which operation is more efficient in a linked list compared to an array?',
            'options': ['Random access', 'Insertion at beginning', 'Binary search', 'Sorting'],
            'correct': 1
        },
        {
            'quiz_id': 1,
            'question': 'What is the space complexity of an array of size n?',
            'options': ['O(1)', 'O(log n)', 'O(n)', 'O(n^2)'],
            'correct': 2
        },
    ]
    
    # Quiz 2: Binary Trees
    quiz_2_questions = [
        {
            'quiz_id': 2,
            'question': 'What is the maximum number of nodes at level k in a binary tree?',
            'options': ['k', '2^k', '2k', 'k^2'],
            'correct': 1
        },
        {
            'quiz_id': 2,
            'question': 'Which traversal visits the root node first?',
            'options': ['Inorder', 'Preorder', 'Postorder', 'Level order'],
            'correct': 1
        },
    ]
    
    # Quiz 3: HTML & CSS
    quiz_3_questions = [
        {
            'quiz_id': 3,
            'question': 'Which HTML tag is used for the largest heading?',
            'options': ['<h6>', '<h1>', '<heading>', '<head>'],
            'correct': 1
        },
        {
            'quiz_id': 3,
            'question': 'What does CSS stand for?',
            'options': ['Computer Style Sheets', 'Cascading Style Sheets', 'Creative Style Sheets', 'Colorful Style Sheets'],
            'correct': 1
        },
        {
            'quiz_id': 3,
            'question': 'Which property is used to change the background color?',
            'options': ['bgcolor', 'color', 'background-color', 'bg-color'],
            'correct': 2
        },
    ]
    
    # Quiz 4: Machine Learning
    quiz_4_questions = [
        {
            'quiz_id': 4,
            'question': 'What type of machine learning uses labeled data?',
            'options': ['Unsupervised', 'Supervised', 'Reinforcement', 'Transfer'],
            'correct': 1
        },
        {
            'quiz_id': 4,
            'question': 'Which of these is a classification algorithm?',
            'options': ['Linear Regression', 'K-Means', 'Decision Tree', 'PCA'],
            'correct': 2
        },
    ]
    
    all_questions = quiz_1_questions + quiz_2_questions + quiz_3_questions + quiz_4_questions
    
    for q in all_questions:
        cursor.execute(
            'INSERT INTO quiz_questions (quiz_id, question_text, options, correct_option_index) VALUES (?, ?, ?, ?)',
            (q['quiz_id'], q['question'], json.dumps(q['options']), q['correct'])
        )
    
    db.commit()
    print(f"✅ Created {len(all_questions)} quiz questions")
    
    # Create some sample quiz submissions
    print("Creating sample quiz submissions...")
    
    submissions = [
        (1, 3, 3, 3, 45),  # Alice scored 3/3 in Quiz 1, took 45 seconds
        (1, 4, 2, 3, 120), # Bob scored 2/3 in Quiz 1, took 120 seconds
        (1, 5, 3, 3, 30),  # Charlie scored 3/3 in Quiz 1, took 30 seconds
        (2, 3, 2, 2, 60),  # Alice scored 2/2 in Quiz 2, took 60 seconds
        (2, 5, 1, 2, 90),  # Charlie scored 1/2 in Quiz 2, took 90 seconds
        (3, 3, 3, 3, 50),  # Alice scored 3/3 in Quiz 3
        (3, 6, 2, 3, 75),  # Diana scored 2/3 in Quiz 3
    ]
    
    for quiz_id, student_id, score, total, duration in submissions:
        cursor.execute(
            'INSERT INTO quiz_submissions (quiz_id, student_id, score, total, duration_seconds) VALUES (?, ?, ?, ?, ?)',
            (quiz_id, student_id, score, total, duration)
        )
    
    db.commit()
    print(f"✅ Created {len(submissions)} quiz submissions")
    
    # Create some chat messages
    print("Creating sample chat messages...")
    
    messages = [
        (1, 3, 'Hello everyone! Looking forward to learning DSA!'),
        (1, 1, 'Welcome to the class, Alice! Feel free to ask questions anytime.'),
        (1, 4, 'Can someone explain the difference between arrays and linked lists?'),
        (1, 3, 'Arrays have contiguous memory, linked lists use pointers!'),
        (2, 3, 'I love web development! 💻'),
        (2, 6, 'Me too! CSS is so powerful.'),
    ]
    
    for class_id, user_id, message in messages:
        cursor.execute(
            'INSERT INTO chat_messages (class_id, user_id, message) VALUES (?, ?, ?)',
            (class_id, user_id, message)
        )
    
    db.commit()
    print(f"✅ Created {len(messages)} chat messages")
    
    # Calculate and insert student metrics
    print("Calculating student metrics...")
    
    # Get all students who have submitted quizzes
    cursor.execute('''
        SELECT DISTINCT student_id, class_id 
        FROM quiz_submissions qs
        JOIN quizzes q ON qs.quiz_id = q.id
    ''')
    
    student_class_pairs = cursor.fetchall()
    
    for student_id, class_id in student_class_pairs:
        # Get quiz submissions for this student in this class
        cursor.execute('''
            SELECT score, total, duration_seconds
            FROM quiz_submissions qs
            JOIN quizzes q ON qs.quiz_id = q.id
            WHERE qs.student_id = ? AND q.class_id = ?
        ''', (student_id, class_id))
        
        submissions = cursor.fetchall()
        
        if submissions:
            total_score = sum(s[0] for s in submissions)
            total_possible = sum(s[1] for s in submissions)
            accuracy = total_score / total_possible if total_possible > 0 else 0
            
            avg_time = sum(s[2] for s in submissions) / len(submissions)
            speed = min(1, 60 / (avg_time + 1))
            
            # Get chat engagement
            cursor.execute(
                'SELECT COUNT(*) FROM chat_messages WHERE user_id = ? AND class_id = ?',
                (student_id, class_id)
            )
            chat_count = cursor.fetchone()[0]
            engagement = min(1, chat_count / 20)
            
            # Calculate pace score (0-10)
            pace_score = round(10 * (0.5 * accuracy + 0.3 * speed + 0.2 * engagement), 1)
            rating = min(10, pace_score)
            
            cursor.execute('''
                INSERT INTO student_metrics
                (user_id, class_id, score_avg, avg_time, pace_score, rating)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, class_id, round(accuracy * 100, 1), round(avg_time, 1), pace_score, rating))
    
    db.commit()
    print(f"✅ Calculated metrics for {len(student_class_pairs)} student-class pairs")
    
    # Close connection
    db.close()
    
    print("\n✨ Database seeding complete!")
    print("\n📋 Demo Accounts:")
    print("\n👨‍🏫 Teachers:")
    print("   teacher1@edu.com / password123")
    print("   teacher2@edu.com / password123")
    print("\n👨‍🎓 Students:")
    print("   student1@edu.com / password123")
    print("   student2@edu.com / password123")
    print("   student3@edu.com / password123")
    print("   student4@edu.com / password123")
    print("   student5@edu.com / password123")
    print("\n🚀 Ready to demo! Run: python app.py\n")

if __name__ == '__main__':
    seed_database()

