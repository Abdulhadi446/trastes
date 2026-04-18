#!/bin/bash
echo "========================================"
echo "  St. George's School Learning Server"
echo "========================================"
echo ""
echo "Starting server..."
echo "Open: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
cd "$(dirname "$0")"
python3 server.py