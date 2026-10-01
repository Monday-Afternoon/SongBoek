@echo off
cd /d "%~dp0"
echo Songlijst bijwerken...
python maak_index.py || py maak_index.py
echo.
echo Het songboek draait nu op http://localhost:8000
echo Laat dit venster open staan zolang je het songboek gebruikt. Sluit het venster om te stoppen.
start "" http://localhost:8000
python -m http.server 8000 || py -m http.server 8000
pause
