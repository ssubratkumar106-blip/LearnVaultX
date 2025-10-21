#!/usr/bin/env python3
"""
Seed Computer Science Courses and Quizzes for Testing
Creates 5 CS courses with 5 quizzes each for teacher1@edu.com
"""

import sqlite3
import json
from datetime import datetime

def seed_cs_courses():
    db = sqlite3.connect('education.db')
    cursor = db.cursor()
    
    print("[SEED] Creating Computer Science Courses and Quizzes...")
    
    # Get teacher1 ID
    teacher = cursor.execute(
        "SELECT id FROM users WHERE email='teacher1@edu.com'"
    ).fetchone()
    
    if not teacher:
        print("[ERROR] Teacher account not found! Run seed_data.py first")
        return
    
    teacher_id = teacher[0]
    print(f"[OK] Found teacher account (ID: {teacher_id})")
    
    # Define 5 Computer Science courses
    courses = [
        {
            'title': 'Python Programming Fundamentals',
            'description': 'Learn Python from scratch including syntax, data structures, OOP, and file handling',
            'topics': ['Variables & Data Types', 'Control Flow', 'Functions', 'OOP Concepts', 'File Handling']
        },
        {
            'title': 'Database Management Systems',
            'description': 'Master SQL, database design, normalization, transactions, and query optimization',
            'topics': ['SQL Basics', 'Joins & Subqueries', 'Normalization', 'Transactions', 'Indexing']
        },
        {
            'title': 'Operating Systems Concepts',
            'description': 'Understanding processes, threads, memory management, file systems, and scheduling',
            'topics': ['Processes & Threads', 'Memory Management', 'File Systems', 'CPU Scheduling', 'Deadlocks']
        },
        {
            'title': 'Computer Networks',
            'description': 'Study network protocols, OSI model, TCP/IP, routing, and network security',
            'topics': ['OSI Model', 'TCP/IP Protocol', 'Routing Algorithms', 'Network Security', 'DNS & HTTP']
        },
        {
            'title': 'Web Development with JavaScript',
            'description': 'Build modern web applications using HTML, CSS, JavaScript, React, and Node.js',
            'topics': ['JavaScript Basics', 'DOM Manipulation', 'ES6 Features', 'React Components', 'REST APIs']
        }
    ]
    
    # Create courses and store their IDs
    course_ids = []
    
    for course in courses:
        cursor.execute(
            'INSERT INTO classes (teacher_id, title, description, created_at) VALUES (?, ?, ?, ?)',
            (teacher_id, course['title'], course['description'], datetime.now())
        )
        course_id = cursor.lastrowid
        course_ids.append({'id': course_id, 'title': course['title'], 'topics': course['topics']})
        print(f"[OK] Created course: {course['title']}")
    
    db.commit()
    
    # Create topics for each course
    print("\n[SEED] Creating topics for courses...")
    
    for course_data in course_ids:
        for topic_name in course_data['topics']:
            cursor.execute(
                'INSERT INTO topics (class_id, topic_name, description, created_at) VALUES (?, ?, ?, ?)',
                (course_data['id'], topic_name, f'Learn about {topic_name}', datetime.now())
            )
        print(f"[OK] Added {len(course_data['topics'])} topics to {course_data['title']}")
    
    db.commit()
    
    # Define 5 quizzes for each course with questions
    quizzes_data = {
        'Python Programming Fundamentals': [
            {
                'title': 'Python Basics Quiz',
                'questions': [
                    ('Which keyword is used to define a function in Python?', ['def', 'function', 'func', 'define'], 0, 'Functions'),
                    ('What is the output of: print(type([]))?', ["<class 'list'>", "<class 'array'>", 'list', 'array'], 0, 'Variables & Data Types'),
                    ('Which loop is used when the number of iterations is unknown?', ['while', 'for', 'do-while', 'foreach'], 0, 'Control Flow'),
                    ('What does the len() function return?', ['Length of object', 'Type of object', 'Value of object', 'None'], 0, 'Variables & Data Types'),
                    ('How do you start a comment in Python?', ['#', '//', '/*', '--'], 0, 'Variables & Data Types')
                ]
            },
            {
                'title': 'Control Flow & Loops',
                'questions': [
                    ('Which statement is used to exit a loop early?', ['break', 'exit', 'stop', 'end'], 0, 'Control Flow'),
                    ('What does "continue" do in a loop?', ['Skips current iteration', 'Exits loop', 'Restarts loop', 'Pauses loop'], 0, 'Control Flow'),
                    ('Which is the correct if-else syntax?', ['if x: ... else: ...', 'if (x) {...} else {...}', 'if x then ... else ...', 'if x do ... else ...'], 0, 'Control Flow'),
                    ('What is a nested loop?', ['Loop inside another loop', 'Loop with multiple conditions', 'Loop that runs forever', 'Loop with break'], 0, 'Control Flow'),
                    ('Which operator checks if values are equal?', ['==', '=', 'equals', 'is'], 0, 'Control Flow')
                ]
            },
            {
                'title': 'Functions & Modules',
                'questions': [
                    ('How do you return a value from a function?', ['return value', 'send value', 'output value', 'give value'], 0, 'Functions'),
                    ('What are function parameters?', ['Input values to function', 'Output of function', 'Function name', 'Function type'], 0, 'Functions'),
                    ('How do you import a module?', ['import module_name', 'include module_name', 'require module_name', 'using module_name'], 0, 'Functions'),
                    ('What is a lambda function?', ['Anonymous function', 'Named function', 'Class method', 'Built-in function'], 0, 'Functions'),
                    ('What does *args allow?', ['Variable number of arguments', 'Multiplication', 'Pointer reference', 'Dictionary arguments'], 0, 'Functions')
                ]
            },
            {
                'title': 'Object-Oriented Programming',
                'questions': [
                    ('What keyword creates a class in Python?', ['class', 'object', 'new', 'create'], 0, 'OOP Concepts'),
                    ('What is __init__ method?', ['Constructor', 'Destructor', 'Main method', 'Static method'], 0, 'OOP Concepts'),
                    ('What is inheritance?', ['Class inherits from another', 'Function calls function', 'Variable copies value', 'Loop inside loop'], 0, 'OOP Concepts'),
                    ('What is "self" in Python classes?', ['Reference to instance', 'Global variable', 'Class name', 'Method name'], 0, 'OOP Concepts'),
                    ('What is encapsulation?', ['Data hiding in classes', 'Class inheritance', 'Method overriding', 'Multiple inheritance'], 0, 'OOP Concepts')
                ]
            },
            {
                'title': 'File Handling & Exceptions',
                'questions': [
                    ('Which mode opens file for reading?', ["'r'", "'w'", "'a'", "'x'"], 0, 'File Handling'),
                    ('How do you handle exceptions?', ['try-except', 'if-else', 'catch-throw', 'error-handle'], 0, 'File Handling'),
                    ('What does with statement do?', ['Auto-closes file', 'Opens file', 'Reads file', 'Writes file'], 0, 'File Handling'),
                    ('Which exception is raised for file not found?', ['FileNotFoundError', 'IOError', 'ValueError', 'TypeError'], 0, 'File Handling'),
                    ('How do you write to a file?', ['file.write()', 'file.print()', 'file.output()', 'file.save()'], 0, 'File Handling')
                ]
            }
        ],
        'Database Management Systems': [
            {
                'title': 'SQL Fundamentals',
                'questions': [
                    ('Which SQL command retrieves data?', ['SELECT', 'GET', 'FETCH', 'RETRIEVE'], 0, 'SQL Basics'),
                    ('What does INSERT do?', ['Adds new records', 'Updates records', 'Deletes records', 'Reads records'], 0, 'SQL Basics'),
                    ('Which clause filters results?', ['WHERE', 'FILTER', 'IF', 'HAVING'], 0, 'SQL Basics'),
                    ('What is PRIMARY KEY?', ['Unique identifier', 'Foreign reference', 'Index key', 'Composite key'], 0, 'SQL Basics'),
                    ('Which command removes records?', ['DELETE', 'REMOVE', 'DROP', 'CLEAR'], 0, 'SQL Basics')
                ]
            },
            {
                'title': 'Joins & Subqueries',
                'questions': [
                    ('What does INNER JOIN do?', ['Returns matching rows', 'Returns all rows', 'Returns left rows', 'Returns right rows'], 0, 'Joins & Subqueries'),
                    ('What is a subquery?', ['Query inside query', 'Multiple queries', 'Join operation', 'Union operation'], 0, 'Joins & Subqueries'),
                    ('Which join returns all left table rows?', ['LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'CROSS JOIN'], 0, 'Joins & Subqueries'),
                    ('What does UNION do?', ['Combines result sets', 'Joins tables', 'Filters data', 'Sorts data'], 0, 'Joins & Subqueries'),
                    ('What is a self join?', ['Table joins itself', 'Multiple table join', 'Outer join', 'Cross join'], 0, 'Joins & Subqueries')
                ]
            },
            {
                'title': 'Database Normalization',
                'questions': [
                    ('What is 1NF?', ['Atomic values only', 'No redundancy', 'No partial dependency', 'No transitive dependency'], 0, 'Normalization'),
                    ('What does normalization reduce?', ['Data redundancy', 'Query speed', 'Storage space', 'Table count'], 0, 'Normalization'),
                    ('What is 2NF requirement?', ['Must be in 1NF and no partial dependency', 'Must be in 3NF', 'Must have primary key', 'Must have foreign key'], 0, 'Normalization'),
                    ('What is denormalization?', ['Adding redundancy for performance', 'Removing redundancy', 'Creating indexes', 'Optimizing queries'], 0, 'Normalization'),
                    ('What is 3NF?', ['No transitive dependency', 'Atomic values', 'No partial dependency', 'Has primary key'], 0, 'Normalization')
                ]
            },
            {
                'title': 'Transactions & ACID',
                'questions': [
                    ('What does ACID stand for?', ['Atomicity, Consistency, Isolation, Durability', 'Access, Control, Integration, Data', 'All, Create, Insert, Delete', 'Automatic, Concurrent, Indexed, Durable'], 0, 'Transactions'),
                    ('What does COMMIT do?', ['Saves transaction', 'Cancels transaction', 'Starts transaction', 'Checks transaction'], 0, 'Transactions'),
                    ('What is atomicity?', ['All or nothing execution', 'Data consistency', 'Transaction isolation', 'Data durability'], 0, 'Transactions'),
                    ('What does ROLLBACK do?', ['Undoes transaction', 'Saves transaction', 'Starts transaction', 'Commits transaction'], 0, 'Transactions'),
                    ('What is isolation?', ['Concurrent transactions dont interfere', 'All changes are permanent', 'Transactions are atomic', 'Data is consistent'], 0, 'Transactions')
                ]
            },
            {
                'title': 'Indexing & Optimization',
                'questions': [
                    ('What is an index?', ['Data structure for fast retrieval', 'Primary key', 'Foreign key', 'Table constraint'], 0, 'Indexing'),
                    ('When should you create an index?', ['On frequently searched columns', 'On all columns', 'Never', 'Only on primary keys'], 0, 'Indexing'),
                    ('What is query optimization?', ['Improving query performance', 'Writing queries', 'Creating indexes', 'Normalizing data'], 0, 'Indexing'),
                    ('What does EXPLAIN do?', ['Shows query execution plan', 'Explains syntax', 'Documents query', 'Optimizes query'], 0, 'Indexing'),
                    ('What is a composite index?', ['Index on multiple columns', 'Multiple indexes', 'Primary and foreign key', 'Unique index'], 0, 'Indexing')
                ]
            }
        ],
        'Operating Systems Concepts': [
            {
                'title': 'Processes & Threads',
                'questions': [
                    ('What is a process?', ['Program in execution', 'Compiled code', 'Source code', 'CPU instruction'], 0, 'Processes & Threads'),
                    ('What is a thread?', ['Lightweight process', 'Heavy process', 'CPU core', 'Memory unit'], 0, 'Processes & Threads'),
                    ('What is context switching?', ['Switching between processes', 'Switching CPU', 'Switching memory', 'Switching threads'], 0, 'Processes & Threads'),
                    ('What is process state?', ['Current status of process', 'Process memory', 'Process ID', 'Process priority'], 0, 'Processes & Threads'),
                    ('What is multithreading?', ['Multiple threads in one process', 'Multiple processes', 'Multiple CPUs', 'Multiple programs'], 0, 'Processes & Threads')
                ]
            },
            {
                'title': 'Memory Management',
                'questions': [
                    ('What is virtual memory?', ['Using disk as RAM', 'Physical RAM', 'Cache memory', 'Register memory'], 0, 'Memory Management'),
                    ('What is paging?', ['Dividing memory into pages', 'Writing to disk', 'Reading from disk', 'Allocating memory'], 0, 'Memory Management'),
                    ('What is page fault?', ['Page not in memory', 'Memory full', 'Disk full', 'CPU error'], 0, 'Memory Management'),
                    ('What is segmentation?', ['Dividing memory by segments', 'Paging technique', 'Disk operation', 'CPU operation'], 0, 'Memory Management'),
                    ('What is thrashing?', ['Excessive paging', 'Fast execution', 'Memory leak', 'Disk failure'], 0, 'Memory Management')
                ]
            },
            {
                'title': 'File Systems',
                'questions': [
                    ('What is a file system?', ['Organizes files on disk', 'Type of file', 'File permission', 'File content'], 0, 'File Systems'),
                    ('What is an inode?', ['File metadata structure', 'File content', 'File name', 'Directory'], 0, 'File Systems'),
                    ('What is a directory?', ['Container for files', 'Type of file', 'File permission', 'Disk partition'], 0, 'File Systems'),
                    ('What is file allocation?', ['How disk space is assigned', 'File size', 'File type', 'File name'], 0, 'File Systems'),
                    ('What is journaling?', ['Tracking file system changes', 'File backup', 'File compression', 'File encryption'], 0, 'File Systems')
                ]
            },
            {
                'title': 'CPU Scheduling',
                'questions': [
                    ('What is CPU scheduling?', ['Selecting next process to run', 'CPU speed control', 'Memory allocation', 'Disk access'], 0, 'CPU Scheduling'),
                    ('What is FCFS?', ['First Come First Served', 'Fastest CPU First', 'Fair CPU Sharing', 'First Class File System'], 0, 'CPU Scheduling'),
                    ('What is Round Robin?', ['Time-sharing scheduling', 'Priority scheduling', 'Random scheduling', 'Shortest job first'], 0, 'CPU Scheduling'),
                    ('What is preemptive scheduling?', ['Can interrupt running process', 'Cannot interrupt process', 'No time limit', 'Infinite execution'], 0, 'CPU Scheduling'),
                    ('What is starvation?', ['Process never gets CPU', 'Process runs forever', 'CPU overload', 'Memory full'], 0, 'CPU Scheduling')
                ]
            },
            {
                'title': 'Deadlocks',
                'questions': [
                    ('What is deadlock?', ['Processes waiting forever', 'Process crash', 'CPU halt', 'Memory full'], 0, 'Deadlocks'),
                    ('What is mutual exclusion?', ['Only one process uses resource', 'Multiple processes share', 'No resource needed', 'Infinite resources'], 0, 'Deadlocks'),
                    ('What is hold and wait?', ['Process holds and requests more', 'Process releases all', 'Process waits only', 'Process holds only'], 0, 'Deadlocks'),
                    ('What is deadlock prevention?', ['Ensure deadlock cant happen', 'Detect deadlock', 'Recover from deadlock', 'Ignore deadlock'], 0, 'Deadlocks'),
                    ('What is circular wait?', ['Processes wait in circle', 'Process waits for itself', 'No waiting', 'Infinite wait'], 0, 'Deadlocks')
                ]
            }
        ],
        'Computer Networks': [
            {
                'title': 'OSI Model Basics',
                'questions': [
                    ('How many layers in OSI model?', ['7', '5', '4', '3'], 0, 'OSI Model'),
                    ('Which layer handles routing?', ['Network', 'Transport', 'Data Link', 'Physical'], 0, 'OSI Model'),
                    ('What is the bottom layer?', ['Physical', 'Data Link', 'Network', 'Transport'], 0, 'OSI Model'),
                    ('Which layer has TCP?', ['Transport', 'Network', 'Session', 'Application'], 0, 'OSI Model'),
                    ('What does Application layer do?', ['User interface', 'Routing', 'Framing', 'Bit transmission'], 0, 'OSI Model')
                ]
            },
            {
                'title': 'TCP/IP Protocol',
                'questions': [
                    ('What does TCP guarantee?', ['Reliable delivery', 'Fast delivery', 'Broadcast', 'Multicast'], 0, 'TCP/IP Protocol'),
                    ('What is IP address?', ['Unique network identifier', 'MAC address', 'Port number', 'Domain name'], 0, 'TCP/IP Protocol'),
                    ('What is three-way handshake?', ['TCP connection establishment', 'UDP communication', 'IP routing', 'DNS lookup'], 0, 'TCP/IP Protocol'),
                    ('What does UDP provide?', ['Fast unreliable delivery', 'Reliable delivery', 'Connection-oriented', 'Error correction'], 0, 'TCP/IP Protocol'),
                    ('What is port number?', ['Application identifier', 'IP address', 'MAC address', 'Network ID'], 0, 'TCP/IP Protocol')
                ]
            },
            {
                'title': 'Routing Algorithms',
                'questions': [
                    ('What is routing?', ['Path selection for packets', 'Packet creation', 'Packet deletion', 'Packet encryption'], 0, 'Routing Algorithms'),
                    ('What is a router?', ['Forwards packets between networks', 'Connects devices', 'Stores packets', 'Creates packets'], 0, 'Routing Algorithms'),
                    ('What is distance vector?', ['Routing algorithm', 'Packet type', 'Network layer', 'IP version'], 0, 'Routing Algorithms'),
                    ('What is link state routing?', ['Each router knows topology', 'Distance based', 'Static routing', 'No routing'], 0, 'Routing Algorithms'),
                    ('What is hop count?', ['Number of routers', 'Packet size', 'Bandwidth', 'Latency'], 0, 'Routing Algorithms')
                ]
            },
            {
                'title': 'Network Security',
                'questions': [
                    ('What is encryption?', ['Converting data to secret form', 'Data compression', 'Data transfer', 'Data storage'], 0, 'Network Security'),
                    ('What is firewall?', ['Network security barrier', 'Router', 'Switch', 'Hub'], 0, 'Network Security'),
                    ('What is SSL/TLS?', ['Encryption protocol', 'Routing protocol', 'Email protocol', 'File protocol'], 0, 'Network Security'),
                    ('What is VPN?', ['Virtual Private Network', 'Very Private Network', 'Virtual Public Network', 'Variable Protocol Network'], 0, 'Network Security'),
                    ('What is DDoS?', ['Distributed Denial of Service', 'Data Download Service', 'Direct Digital Service', 'Dynamic DNS Service'], 0, 'Network Security')
                ]
            },
            {
                'title': 'DNS & HTTP',
                'questions': [
                    ('What does DNS do?', ['Resolves domain to IP', 'Routes packets', 'Encrypts data', 'Stores files'], 0, 'DNS & HTTP'),
                    ('What is HTTP?', ['Web protocol', 'Email protocol', 'File protocol', 'DNS protocol'], 0, 'DNS & HTTP'),
                    ('What is HTTPS?', ['Secure HTTP', 'Fast HTTP', 'New HTTP', 'Local HTTP'], 0, 'DNS & HTTP'),
                    ('What is a URL?', ['Web address', 'IP address', 'MAC address', 'Port number'], 0, 'DNS & HTTP'),
                    ('What is GET request?', ['Retrieve data', 'Send data', 'Delete data', 'Update data'], 0, 'DNS & HTTP')
                ]
            }
        ],
        'Web Development with JavaScript': [
            {
                'title': 'JavaScript Basics',
                'questions': [
                    ('Which keyword declares a variable?', ['let', 'var', 'const', 'All of above'], 3, 'JavaScript Basics'),
                    ('What is the output of: typeof null?', ['object', 'null', 'undefined', 'number'], 0, 'JavaScript Basics'),
                    ('How do you declare a function?', ['function name() {}', 'def name() {}', 'func name() {}', 'function: name() {}'], 0, 'JavaScript Basics'),
                    ('What is NaN?', ['Not a Number', 'Null and None', 'Number and Null', 'New Array Number'], 0, 'JavaScript Basics'),
                    ('Which is a falsy value?', ['0', '1', '"false"', '[]'], 0, 'JavaScript Basics')
                ]
            },
            {
                'title': 'DOM Manipulation',
                'questions': [
                    ('What is DOM?', ['Document Object Model', 'Data Object Model', 'Document Oriented Model', 'Direct Object Method'], 0, 'DOM Manipulation'),
                    ('How do you select element by ID?', ['getElementById()', 'selectById()', 'getElement()', 'findById()'], 0, 'DOM Manipulation'),
                    ('What does createElement() do?', ['Creates new element', 'Selects element', 'Deletes element', 'Updates element'], 0, 'DOM Manipulation'),
                    ('How do you add event listener?', ['addEventListener()', 'addEvent()', 'onEvent()', 'listen()'], 0, 'DOM Manipulation'),
                    ('What is event bubbling?', ['Events propagate upward', 'Events propagate downward', 'Events stop', 'Events loop'], 0, 'DOM Manipulation')
                ]
            },
            {
                'title': 'ES6 Features',
                'questions': [
                    ('What is arrow function?', ['() => {}', 'function() {}', '=> function() {}', 'arrow() {}'], 0, 'ES6 Features'),
                    ('What does const mean?', ['Constant reference', 'Constant value', 'No change ever', 'Immutable object'], 0, 'ES6 Features'),
                    ('What is template literal?', ['`string ${var}`', '"string"', "'string'", 'String()'], 0, 'ES6 Features'),
                    ('What is destructuring?', ['Extract values from objects/arrays', 'Delete properties', 'Create objects', 'Merge arrays'], 0, 'ES6 Features'),
                    ('What is spread operator?', ['...', '>>>', '+++', '==='], 0, 'ES6 Features')
                ]
            },
            {
                'title': 'React Components',
                'questions': [
                    ('What is a component?', ['Reusable UI piece', 'CSS file', 'JavaScript file', 'HTML file'], 0, 'React Components'),
                    ('How do you create component?', ['function Component() {}', 'class Component()', 'component Component {}', 'new Component()'], 0, 'React Components'),
                    ('What is JSX?', ['JavaScript XML', 'Java Syntax Extension', 'JavaScript Extension', 'JSON XML'], 0, 'React Components'),
                    ('What is state?', ['Component data', 'CSS style', 'HTML structure', 'Event handler'], 0, 'React Components'),
                    ('What is props?', ['Data passed to component', 'Component state', 'Event handler', 'CSS class'], 0, 'React Components')
                ]
            },
            {
                'title': 'REST APIs',
                'questions': [
                    ('What is REST?', ['Representational State Transfer', 'Remote External Service Transfer', 'Reliable External System', 'Rapid Exchange Service'], 0, 'REST APIs'),
                    ('What is GET method?', ['Retrieve data', 'Create data', 'Update data', 'Delete data'], 0, 'REST APIs'),
                    ('What is POST method?', ['Create new resource', 'Get resource', 'Update resource', 'Delete resource'], 0, 'REST APIs'),
                    ('What is JSON?', ['JavaScript Object Notation', 'Java Standard Output', 'JavaScript Online Network', 'JSON String Object'], 0, 'REST APIs'),
                    ('What is status code 200?', ['Success', 'Not Found', 'Server Error', 'Unauthorized'], 0, 'REST APIs')
                ]
            }
        ]
    }
    
    # Create quizzes and questions
    print("\n[SEED] Creating quizzes and questions...")
    
    for course_data in course_ids:
        course_title = course_data['title']
        course_id = course_data['id']
        
        if course_title not in quizzes_data:
            continue
        
        quiz_list = quizzes_data[course_title]
        
        for quiz_info in quiz_list:
            # Create quiz
            cursor.execute(
                'INSERT INTO quizzes (class_id, title, created_at) VALUES (?, ?, ?)',
                (course_id, quiz_info['title'], datetime.now())
            )
            quiz_id = cursor.lastrowid
            
            # Get topics for this course
            topics = cursor.execute(
                'SELECT id, topic_name FROM topics WHERE class_id = ?',
                (course_id,)
            ).fetchall()
            topic_map = {name: tid for tid, name in topics}
            
            # Create questions
            for question, options, correct_idx, topic_name in quiz_info['questions']:
                cursor.execute(
                    '''INSERT INTO quiz_questions 
                    (quiz_id, question_text, options, correct_option_index) 
                    VALUES (?, ?, ?, ?)''',
                    (quiz_id, question, json.dumps(options), correct_idx)
                )
                question_id = cursor.lastrowid
                
                # Map question to topic
                if topic_name in topic_map:
                    topic_id = topic_map[topic_name]
                    try:
                        cursor.execute(
                            'INSERT INTO question_topics (question_id, topic_id) VALUES (?, ?)',
                            (question_id, topic_id)
                        )
                    except:
                        pass  # Ignore duplicates
            
            print(f"[OK] Created quiz: {quiz_info['title']} with {len(quiz_info['questions'])} questions")
    
    db.commit()
    
    # Enroll all students in all new courses
    print("\n[SEED] Enrolling students in courses...")
    
    students = cursor.execute("SELECT id FROM users WHERE role='student'").fetchall()
    
    for student_id, in students:
        for course_data in course_ids:
            try:
                cursor.execute(
                    'INSERT INTO enrollments (student_id, class_id, enrolled_at) VALUES (?, ?, ?)',
                    (student_id, course_data['id'], datetime.now())
                )
            except:
                pass  # Ignore if already enrolled
    
    db.commit()
    print(f"[OK] Enrolled {len(students)} students in {len(course_ids)} courses")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\n[SUCCESS] Created:")
    print(f"   - {len(course_ids)} Computer Science courses")
    print(f"   - 5 quizzes per course = {len(course_ids) * 5} total quizzes")
    print(f"   - 5 questions per quiz = {len(course_ids) * 25} total questions")
    print(f"   - All students enrolled in all courses")
    print(f"\n[TEACHER LOGIN]")
    print(f"   Email: teacher1@edu.com")
    print(f"   Password: password123")
    print(f"\n[STUDENT LOGIN]")
    print(f"   Email: student1@edu.com")
    print(f"   Password: password123")
    print(f"\n[NEXT STEPS]")
    print(f"   1. Login as student")
    print(f"   2. Take quizzes (get some wrong!)")
    print(f"   3. Check 'Knowledge Gaps' section")
    print(f"   4. Check 'AI Recommendations' section")
    print(f"   5. Check 'My Progress' for analytics")
    print("\n" + "="*60)
    
    db.close()

if __name__ == '__main__':
    seed_cs_courses()

