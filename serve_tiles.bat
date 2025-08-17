@echo off
cls

:: =================================================================
:: This script prompts for a map name, extracts a specific
:: bounding box from a remote .pmtiles file, and then starts
:: a local tile server.
:: =================================================================

echo.
echo Protomaps Area Extractor and Server Launcher
echo ============================================
echo.

:: 1. Prompt the user for the map name string
set /p MAP_NAME="Enter the map name (the date of yesterday in the format YYYYMMDD - You can also find it at https://docs.protomaps.com/guide/getting-started#_2-find-the-latest-daily-planet in the command window): "

:: Check if the user entered anything
if "%MAP_NAME%"=="" (
    echo.
    echo ERROR: No map name entered. Aborting.
    pause
    exit /b
)

:: Define variables for clarity
set "SOURCE_URL=https://build.protomaps.com/%MAP_NAME%.pmtiles"
set "OUTPUT_FILE=my_area.pmtiles"
set "BBOX=8.934631,45.328962,9.725475,45.722420"

echo.
echo --- Step 1: Extracting Map Area ---
echo Source: %SOURCE_URL%
echo Output: %OUTPUT_FILE%
echo.

:: 2. Run the pmtiles extract command
pmtiles extract %SOURCE_URL% %OUTPUT_FILE% --bbox=%BBOX%

:: Check if the last command was successful. %ERRORLEVEL% 0 means success.
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: pmtiles extract command failed. Please check the map name and your internet connection.
    pause
    exit /b
)

echo.
echo --- Step 2: Starting Tile Server ---
echo Extraction complete. Starting tileserver-gl...
echo Your map will be available at http://localhost:8080
echo Press CTRL+C in this window to stop the server.
echo.

:: 3. Run the tileserver-gl command
tileserver-gl

echo.
echo Server stopped.
pause