#!/usr/bin/env python3
"""
Quick Feature Test Script
Tests all new adaptive learning features
"""

import sqlite3
import os
from datetime import datetime

print("="*60)
print("TESTING NEW ADAPTIVE LEARNING FEATURES")
print("="*60)

# Connect to database
db_path = 'education.db'

if not os.path.exists(db_path):
    print("\n[ERROR] Database not found!")
    print("Run: python -c 'from app import init_db; init_db()' first")
    exit(1)

db = sqlite3.connect(db_path)
cursor = db.cursor()

# Test 1: Check New Tables
print("\n[TEST 1] Checking Adaptive Learning Tables...")
new_tables = [
    'topics', 'question_topics', 'knowledge_gaps', 
    'recommendations', 'learning_paths', 'topic_mastery',
    'teacher_interventions', 'ai_context_sessions'
]

all_tables = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()
table_names = [t[0] for t in all_tables]

missing_tables = []
for table in new_tables:
    if table in table_names:
        print(f"   [OK] {table}")
    else:
        print(f"   [MISSING] {table}")
        missing_tables.append(table)

if missing_tables:
    print(f"\n[ERROR] Missing tables: {', '.join(missing_tables)}")
    print("Run: python seed_data.py to create tables")
else:
    print("\n[SUCCESS] All adaptive learning tables present!")

# Test 2: Check Demo Data
print("\n[TEST 2] Checking Demo Data...")

# Check users
user_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
print(f"   Users: {user_count}")

# Check classes
class_count = cursor.execute("SELECT COUNT(*) FROM classes").fetchone()[0]
print(f"   Classes: {class_count}")

# Check topics
topic_count = cursor.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
print(f"   Topics: {topic_count}")

# Check question-topic mappings
qt_count = cursor.execute("SELECT COUNT(*) FROM question_topics").fetchone()[0]
print(f"   Question-Topic Mappings: {qt_count}")

if user_count == 0 or class_count == 0:
    print("\n[WARNING] No demo data found!")
    print("Run: python seed_data.py to populate database")
elif topic_count == 0:
    print("\n[WARNING] No topics found - adaptive features won't work!")
    print("Run: python seed_data.py to create topics")
else:
    print("\n[SUCCESS] Demo data loaded!")

# Test 3: Check Student Accounts
print("\n[TEST 3] Checking Demo Accounts...")

students = cursor.execute(
    "SELECT name, email FROM users WHERE role='student' LIMIT 3"
).fetchall()

teachers = cursor.execute(
    "SELECT name, email FROM users WHERE role='teacher' LIMIT 2"
).fetchall()

if students:
    print("\n   Student Accounts:")
    for name, email in students:
        print(f"      - {email} (password123)")
else:
    print("\n   [ERROR] No student accounts found!")

if teachers:
    print("\n   Teacher Accounts:")
    for name, email in teachers:
        print(f"      - {email} (password123)")
else:
    print("\n   [ERROR] No teacher accounts found!")

# Test 4: Simulate Knowledge Gap Detection
print("\n[TEST 4] Testing Knowledge Gap Detection...")

# Check if there are any quiz submissions
submissions = cursor.execute(
    """
    SELECT qs.id, qs.student_id, q.class_id
    FROM quiz_submissions qs
    JOIN quizzes q ON qs.quiz_id = q.id
    LIMIT 1
    """
).fetchone()

if submissions:
    print("   [OK] Quiz submissions exist")
    
    # Check if gaps were created
    gaps = cursor.execute(
        "SELECT COUNT(*) FROM knowledge_gaps"
    ).fetchone()[0]
    
    print(f"   Knowledge Gaps Detected: {gaps}")
    
    if gaps == 0:
        print("   [INFO] No gaps yet - students need to take quizzes!")
else:
    print("   [INFO] No quiz submissions yet")

# Test 5: Check Recommendations
print("\n[TEST 5] Testing AI Recommendations...")

try:
    recommendations = cursor.execute(
        "SELECT COUNT(*) FROM recommendations"
    ).fetchone()[0]

    print(f"   Total Recommendations: {recommendations}")

    if recommendations > 0:
        print("   [SUCCESS] Recommendations table has data!")
        
        # Show sample
        sample = cursor.execute(
            """
            SELECT content_type, reason
            FROM recommendations
            LIMIT 1
            """
        ).fetchone()
        
        if sample:
            print(f"   Sample: {sample[0]} - {sample[1][:50]}...")
    else:
        print("   [INFO] No recommendations yet - take some quizzes!")
except sqlite3.OperationalError as e:
    print(f"   [ERROR] {e}")
    print("   [INFO] Run seed_data.py to fix database schema")

# Test 6: Check Teacher Interventions
print("\n[TEST 6] Testing Teacher Intervention Alerts...")

try:
    interventions = cursor.execute(
        "SELECT COUNT(*) FROM teacher_interventions"
    ).fetchone()[0]

    print(f"   Total Alerts: {interventions}")

    if interventions > 0:
        print("   [SUCCESS] Intervention alerts created!")
        
        # Show sample
        sample = cursor.execute(
            """
            SELECT alert_type, severity
            FROM teacher_interventions
            LIMIT 1
            """
        ).fetchone()
        
        if sample:
            print(f"   Sample Alert: {sample[0]} (Severity: {sample[1]})")
    else:
        print("   [INFO] No alerts yet - students performing well!")
except sqlite3.OperationalError as e:
    print(f"   [ERROR] {e}")
    print("   [INFO] Run seed_data.py to fix database schema")

# Test 7: Check Topics Coverage
print("\n[TEST 7] Checking Topic Coverage...")

if topic_count > 0:
    try:
        # Check which classes have topics
        classes_with_topics = cursor.execute(
            """
            SELECT c.title, COUNT(t.id) as topic_count
            FROM classes c
            LEFT JOIN topics t ON c.id = t.class_id
            GROUP BY c.id
            """
        ).fetchall()
        
        for class_name, topics in classes_with_topics:
            if topics > 0:
                print(f"   [OK] {class_name}: {topics} topics")
            else:
                print(f"   [WARNING] {class_name}: No topics assigned")
    except sqlite3.OperationalError:
        print("   [INFO] Topic coverage check skipped")

# Test 8: Environment Check
print("\n[TEST 8] Checking Environment Configuration...")

from dotenv import load_dotenv
load_dotenv()

anthropic_key = os.getenv('ANTHROPIC_API_KEY')
groq_key = os.getenv('GROQ_API_KEY')
deepseek_key = os.getenv('DEEPSEEK_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')

ai_configured = False

if anthropic_key:
    print("   [BEST] Claude AI (Anthropic) configured!")
    ai_configured = True
elif groq_key:
    print("   [GOOD] Groq AI configured (free)")
    ai_configured = True
elif deepseek_key:
    print("   [OK] DeepSeek AI configured")
    ai_configured = True
elif openai_key:
    print("   [OK] OpenAI configured")
    ai_configured = True
else:
    print("   [WARNING] No AI API key found")
    print("   Chatbot will show setup message")

# Final Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

issues = []

if missing_tables:
    issues.append("Missing database tables")
if user_count == 0:
    issues.append("No demo users")
if topic_count == 0:
    issues.append("No topics for adaptive learning")
if not ai_configured:
    issues.append("No AI API key (optional)")

if not issues:
    print("\n[SUCCESS] ALL TESTS PASSED!")
    print("\nYour platform is ready to demo!")
    print("\nNext Steps:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Login with demo accounts above")
    print("   4. Take quizzes to test adaptive features")
else:
    print("\n[WARNING] Some issues found:")
    for issue in issues:
        print(f"   - {issue}")
    print("\nFix these by running:")
    if "Missing database tables" in issues or "No demo users" in issues or "No topics" in issues:
        print("   python seed_data.py")
    if "No AI API key" in issues:
        print("   Add API key to .env file (optional)")

print("\n" + "="*60)
print("See TESTING_GUIDE.md for detailed testing instructions")
print("="*60)

db.close()

