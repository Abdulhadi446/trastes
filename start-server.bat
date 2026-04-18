@echo off
echo ========================================
echo   St. George's School Learning Server
echo ========================================
echo.
echo Opening: http://localhost:5000
echo.
echo Keep this terminal OPEN
echo Press Ctrl+C to stop
echo ========================================
echo.
pip install flask requests 2>nul
python server.py
pause