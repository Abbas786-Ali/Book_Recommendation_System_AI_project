#!/usr/bin/env python
"""
Run script for the Book Recommendation System

Usage:
    python run.py              # Run in development mode
    python run.py --port 8000  # Run on specific port
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import app

if __name__ == '__main__':
    port = 5000
    
    # Check for custom port argument
    if len(sys.argv) > 1:
        if sys.argv[1] == '--port' and len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print(f"Error: Invalid port number '{sys.argv[2]}'")
                sys.exit(1)
    
    print(f"\n🚀 Starting Book Recommendation System on http://127.0.0.1:{port}/")
    print("Press CTRL+C to stop the server\n")
    
    app.run(debug=True, port=port)
