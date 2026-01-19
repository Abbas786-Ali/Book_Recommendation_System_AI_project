#!/bin/bash
# Quick Setup Script for Book Recommendation System

set -e

echo "🚀 Book Recommendation System - Setup Script"
echo "=============================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📖 Next steps:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python run.py"
echo ""
echo "  3. Open in browser:"
echo "     http://127.0.0.1:5000/"
echo ""
