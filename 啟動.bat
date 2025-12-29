@echo off
:: ==================================================
::  One-Click Launcher for Local NSFW Story Writer
::  - Starts Ollama with gemma2:27b model
::  - Launches Gradio web interface
::  - Automatically opens your default browser
::  - Fully English + no garbled text issues
:: ==================================================

chcp 65001 >nul
cls
echo.
echo  ==================================================
echo   Local NSFW Interactive Story Writer Starting...
echo  ==================================================
echo.
echo  Step 1: Starting Ollama and loading gemma2:27b model
echo         (First time will download ~16GB, please be patient)
echo.
echo  Step 2: Launching Gradio web interface
echo         Browser will open automatically at: http://127.0.0.1:7860
echo.
echo  IMPORTANT: Keep this window open! Closing it stops everything.
echo.

:: Start Ollama model in a minimized background window
start "Ollama - gemma2:27b" /min cmd /c "ollama run gemma2:27b"

:: Wait 12 seconds to ensure the model starts loading
timeout /t 12 >nul

:: Start Gradio app (window stays open so you can see any errors)
start "NSFW Story Writer" cmd /k "chcp 65001 >nul && python app.py"

:: Wait a moment for Gradio to fully start, then open browser automatically
echo.
echo  Waiting for Gradio to start... (about 10-15 seconds)
timeout /t 15 >nul

:: Automatically open default browser
start http://127.0.0.1:7860

echo.
echo  ==================================================
echo   Everything started successfully!
echo.
echo   Your browser should open automatically now.
echo   If it doesn't, manually go to:
echo   http://127.0.0.1:7860
echo.
echo   Enjoy creating your NSFW stories with gemma2:27b!
echo  ==================================================
echo.
pause