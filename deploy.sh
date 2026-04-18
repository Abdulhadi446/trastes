#!/bin/bash
# Clone and run on remote server

echo "========================================"
echo "  Deploying to tests server..."
echo "========================================"

ssh tests << 'EOF'
  cd ~
  git clone https://github.com/Abdulhadi446/trastes.git st-school
  cd st-school
  pip3 install flask requests 2>/dev/null || pip install flask requests 2>/dev/null
  nohup python3 server.py > server.log 2>&1 &
  sleep 2
  echo "Server starting..."
  
  # Get IP
  IP=$(hostname -I | awk '{print $1}')
  echo "========================================"
  echo "Server running!"
  echo "URL: http://$IP:5000"
  echo "========================================"
EOF