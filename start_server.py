#!/usr/bin/env python3
"""
Production server startup script for Render.com deployment
"""
import os
import sys
import sqlite3
from app import app, init_db

def setup_database():
    """Initialize database if it doesn't exist"""
    try:
        # Check if database exists
        if not os.path.exists('education.db'):
            print("Creating database...")
            init_db()
            print("Database created successfully!")
        else:
            print("Database already exists")
            
        # Test database connection
        conn = sqlite3.connect('education.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Database connected successfully! Found {len(tables)} tables.")
        conn.close()
        
    except Exception as e:
        print(f"Database setup error: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🚀 Starting LearnVaultX on Render.com...")
    
    # Setup database
    setup_database()
    
    # Get port from environment (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🌐 Starting server on port {port}")
    print("✅ LearnVaultX is ready!")
    
    # Start the application with Gunicorn for production
    import subprocess
    import sys
    
    # Use Gunicorn for production deployment
    gunicorn_cmd = [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        '--keep-alive', '2',
        '--max-requests', '1000',
        '--max-requests-jitter', '100',
        'app:app'
    ]
    
    print(f"🚀 Starting with Gunicorn: {' '.join(gunicorn_cmd)}")
    subprocess.run(gunicorn_cmd)

if __name__ == '__main__':
    main()