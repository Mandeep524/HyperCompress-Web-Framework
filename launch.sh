#!/bin/bash

# Data Compression Project - Launcher Script
# This script helps you choose and launch the UI

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     DATA COMPRESSION PROJECT - UI LAUNCHER                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Choose your interface:"
echo ""
echo "  1) 🖥️  Desktop GUI (Tkinter) - Native window application"
echo "  2) 🌐 Web Interface (Flask) - Browser-based interface"
echo "  3) 💻 Command Line Demo - Terminal-based demo"
echo "  4) 📊 Full Demo - Comprehensive terminal demo"
echo "  5) ❓ Help - View UI guide"
echo "  6) 🚪 Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🖥️  Launching Desktop GUI..."
        echo "   A window should open shortly."
        echo "   Close the window to exit."
        echo ""
        python gui.py
        ;;
    2)
        echo ""
        echo "🌐 Starting Web Server..."
        echo "   Opening browser to http://localhost:5000"
        echo "   Press CTRL+C to stop the server"
        echo ""
        python web_ui.py
        ;;
    3)
        echo ""
        echo "💻 Running Command Line Demo..."
        echo ""
        python demo.py
        ;;
    4)
        echo ""
        echo "📊 Running Full Comprehensive Demo..."
        echo ""
        python run_full_demo.py
        ;;
    5)
        echo ""
        echo "📖 Opening UI Guide..."
        echo ""
        if command -v less &> /dev/null; then
            less UI_GUIDE.md
        else
            cat UI_GUIDE.md
        fi
        ;;
    6)
        echo ""
        echo "👋 Goodbye!"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        echo ""
        exit 1
        ;;
esac
