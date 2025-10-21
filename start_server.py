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
    
    # Start the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )

if __name__ == '__main__':
    main()