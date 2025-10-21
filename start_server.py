"""
Simple server starter with error catching
"""
import sys
import traceback

print("=" * 60)
print("Starting LearnVaultX Server...")
print("=" * 60)

try:
    print("\n1. Importing app module...")
    from app import app, socketio
    print("   ✅ App imported successfully")
    
    print("\n2. Checking database...")
    import os
    if os.path.exists('education.db'):
        print("   ✅ Database exists")
    else:
        print("   ⚠️  Database not found, initializing...")
        from app import init_db
        init_db()
        print("   ✅ Database initialized")
    
    print("\n3. Starting Flask-SocketIO server...")
    print("   🌐 Server will start on: http://localhost:5000")
    print("   🌐 Or access via: http://127.0.0.1:5000")
    print("   ⚠️  Press Ctrl+C to stop the server")
    print("\n" + "=" * 60)
    
    # Start the server
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    
except KeyboardInterrupt:
    print("\n\n🛑 Server stopped by user")
    sys.exit(0)
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ ERROR OCCURRED:")
    print("=" * 60)
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print("\nFull Traceback:")
    print("-" * 60)
    traceback.print_exc()
    print("-" * 60)
    print("\n💡 Common fixes:")
    print("   1. Make sure no other app is using port 5000")
    print("   2. Run: pip install -r requirements.txt")
    print("   3. Try: python seed_data.py")
    print("   4. Check if firewall is blocking port 5000")
    sys.exit(1)

