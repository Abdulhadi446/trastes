# How to Run the AI Chatbot

## Step 1: Start the Server
Open terminal in this folder and run:
```bash
pip install flask requests
python server.py
```
Or on Windows, just double-click `start-server.bat`

## Step 2: Open the Website
Open `index.html` in browser (will work with Live Server too)

## Step 3: Use the Chatbot
- Click 🤖 purple button
- Select subject (English/Maths/Science/Urdu)
- Ask questions!

## The server runs at:
http://localhost:5000

## How it works:
- The chatbot sends your question to localhost:5000
- The Flask server forwards it to Sodeom AI API  
- Response comes back to the chatbot