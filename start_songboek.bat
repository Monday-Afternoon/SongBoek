@echo off
cd /d "%~dp0"
echo Songlijst bijwerken...
python maak_index.py || py maak_index.py
echo.
echo Het songboek draait op http://localhost:8000
echo Laat dit venster open staan zolang je het songboek gebruikt.
echo Sluit dit venster om te stoppen.
echo.
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8000"
python -m http.server 8000 || py -m http.server 8000
echo.
echo Het songboek is gestopt.
echo Staat hierboven "Address already in use"? Sluit dan alle andere zwarte songboek-vensters en start dit bestand opnieuw.
pause
