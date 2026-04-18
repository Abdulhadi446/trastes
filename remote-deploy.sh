#!/bin/bash
# SSH into server, clone and run

echo "========================================"
echo "  Connecting to server..."
echo "========================================"

# Commands to run on remote server
ssh $1 << 'EOF'
  cd ~
  git clone https://github.com/Abdulhadi446/trastes.git st-school
  cd st-school
  pip3 install flask requests
  echo "Starting server..."
  python3 server.py &
  sleep 2
  echo "Server running at http://localhost:5000"
  echo "To access remotely, use: http://$(hostname -I):5000"
EOF

echo "Connected and started!"