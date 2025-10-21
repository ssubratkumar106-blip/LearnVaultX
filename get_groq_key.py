#!/usr/bin/env python3
"""
Groq API Key Setup Helper
========================

This script helps you get a FREE Groq API key for your LearnVaultX app.

Groq is:
- Completely FREE (no credit card needed)
- Super FAST responses
- Very reliable
- Easy to set up

Steps:
1. Run this script
2. Follow the instructions
3. Copy your API key
4. Add it to your .env file
"""

import webbrowser
import os
import sys
import codecs

# Fix Unicode issues on Windows
if sys.platform == "win32":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def main():
    print("GROQ API KEY SETUP HELPER")
    print("=" * 50)
    print()
    print("Groq AI is the BEST free option for your LearnVaultX app!")
    print("✓ Completely FREE (no credit card needed)")
    print("✓ Super FAST responses")
    print("✓ Very reliable")
    print("✓ Easy to set up")
    print()
    
    # Open Groq console
    print("Opening Groq Console...")
    webbrowser.open("https://console.groq.com")
    print("✓ Groq Console opened in your browser")
    print()
    
    print("FOLLOW THESE STEPS:")
    print("1. Sign up for a FREE account (no credit card needed)")
    print("2. Go to API Keys: https://console.groq.com/keys")
    print("3. Click 'Create API Key'")
    print("4. Copy the key (starts with 'gsk_')")
    print("5. Come back here and press Enter")
    print()
    
    input("Press Enter when you have your API key...")
    print()
    
    # Get API key from user
    api_key = input("Paste your Groq API key here: ").strip()
    
    if not api_key:
        print("ERROR: No API key provided. Please try again.")
        return
    
    if not api_key.startswith('gsk_'):
        print("WARNING: Groq API keys usually start with 'gsk_'")
        print("   Make sure you copied the correct key.")
        print()
    
    # Update .env file
    env_file = '.env'
    if os.path.exists(env_file):
        # Read current .env
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update or add GROQ_API_KEY
        if 'GROQ_API_KEY=' in content:
            # Replace existing
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('GROQ_API_KEY='):
                    lines[i] = f'GROQ_API_KEY={api_key}'
                    break
            content = '\n'.join(lines)
        else:
            # Add new
            content += f'\nGROQ_API_KEY={api_key}\n'
        
        # Write back
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✓ API key added to .env file!")
    else:
        print("ERROR: .env file not found. Please create it first.")
        return
    
    print()
    print("SETUP COMPLETE!")
    print("=" * 50)
    print("Your LearnVaultX app now has Groq AI support!")
    print()
    print("NEXT STEPS:")
    print("1. Restart your app: python app.py")
    print("2. Open: http://localhost:5000")
    print("3. Try the AI chatbot - it will be FAST!")
    print()
    print("Groq AI is now your primary AI provider!")
    print("If it fails, the app will try other providers automatically.")

if __name__ == "__main__":
    main()
