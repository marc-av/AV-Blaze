@echo off
echo ============================================
echo   Building Text Expander - Standalone EXE
echo ============================================
echo.

REM Activate venv if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run PyInstaller
pyinstaller --noconfirm --onefile --windowed ^
    --name "TextExpander" ^
    --add-data "TextBlazeWeb;TextBlazeWeb" ^
    app.py

echo.
if exist "dist\TextExpander.exe" (
    echo ============================================
    echo   BUILD SUCCESSFUL!
    echo   Output: dist\TextExpander.exe
    echo ============================================
) else (
    echo   BUILD FAILED - check output above.
)
pause
