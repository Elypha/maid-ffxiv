@echo off
cd /d "D:\JK Maid\FFXIV"
shortcuts\cmdow.exe @ /TOP

cls
echo   ===== Select Entry =====
echo.
echo    ^> FFXIV
echo.
echo      1. Planting
echo      2. Leves
echo      3. Cards
echo.
echo    ^> Genshin
echo.
echo      4. Explore
echo.
echo    ^> Dev
echo.
echo      0. Test
echo.
echo.
set /p choice=

if "%choice%"=="1" (
    cls
    TITLE Planting
    echo   == Planting ==
    echo.
    python\Scripts\python.exe "JK_Planting.py"
    goto end
)

if "%choice%"=="2" (
    cls
    TITLE Leves
    echo   == Leves ==
    echo.
    python\Scripts\python.exe "JK_Leves.py"
    goto end
)

if "%choice%"=="3" (
    cls
    TITLE Cards
    echo   == Cards ==
    echo.
    python\Scripts\python.exe "JK_Cards.py"
    goto end
)

if "%choice%"=="4" (
    cls
    TITLE Explore
    echo   == Explore ==
    echo.
    python\Scripts\python.exe "JK_Explore.py"
    goto end
)

if "%choice%"=="0" (
    cls
    TITLE Test
    echo   == Test ==
    echo.
    python\Scripts\python.exe "test.py"
    goto end
)

:end
pause>nul
exit
