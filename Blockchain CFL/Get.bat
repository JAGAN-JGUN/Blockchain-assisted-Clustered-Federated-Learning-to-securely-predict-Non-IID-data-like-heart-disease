@echo off
setlocal enabledelayedexpansion

:: Define the parent directory
set "PARENT_DIR=%CD%"

:: Create an array of subdirectories (sorted A-Z)
set "INDEX=0"
for /D %%D in (*) do (
    set /A INDEX+=1
    set "DIRS[!INDEX!]=%%D"
)

:: Get total number of directories
set "TOTAL_DIRS=!INDEX!"

echo Total directories found: %TOTAL_DIRS%

:: Ensure there are exactly 16 directories
if %TOTAL_DIRS% NEQ 16 (
    echo Error: Expected 16 directories but found %TOTAL_DIRS%.
    pause
    exit /b
)

:: Loop through each directory and create address_get.txt
for /L %%I in (1,1,16) do (
    set "CURRENT_DIR=!DIRS[%%I]!"
    set "ADDRESS_GET_FILE=%PARENT_DIR%\!CURRENT_DIR!\address_get.txt"

    :: Case 1: 1st-11th directories get the 16th directory's contract_address.txt
    if %%I LEQ 11 (
        set "SOURCE_DIR=!DIRS[16]!"
        type "%PARENT_DIR%\!SOURCE_DIR!\contract_address.txt" > "!ADDRESS_GET_FILE!"
    )

    :: Case 2: 12th directory gets the 1st and 2nd contract_address.txt (separated by a blank line)
    if %%I EQU 12 (
        set "SOURCE_DIR1=!DIRS[1]!"
        set "SOURCE_DIR2=!DIRS[2]!"
        (
            type "%PARENT_DIR%\!SOURCE_DIR1!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR2!\contract_address.txt"
        ) > "!ADDRESS_GET_FILE!"
    )

    :: Case 3: 13th directory gets the 3rd to 6th contract_address.txt (separated by blank lines)
    if %%I EQU 13 (
        set "SOURCE_DIR1=!DIRS[3]!"
        set "SOURCE_DIR2=!DIRS[4]!"
        set "SOURCE_DIR3=!DIRS[5]!"
        set "SOURCE_DIR4=!DIRS[6]!"
        (
            type "%PARENT_DIR%\!SOURCE_DIR1!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR2!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR3!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR4!\contract_address.txt"
        ) > "!ADDRESS_GET_FILE!"
    )

    :: Case 4: 14th directory gets the 7th contract_address.txt
    if %%I EQU 14 (
        set "SOURCE_DIR=!DIRS[7]!"
        type "%PARENT_DIR%\!SOURCE_DIR!\contract_address.txt" > "!ADDRESS_GET_FILE!"
    )

    :: Case 5: 15th directory gets the 8th to 11th contract_address.txt (separated by blank lines)
    if %%I EQU 15 (
        set "SOURCE_DIR1=!DIRS[8]!"
        set "SOURCE_DIR2=!DIRS[9]!"
        set "SOURCE_DIR3=!DIRS[10]!"
        set "SOURCE_DIR4=!DIRS[11]!"
        (
            type "%PARENT_DIR%\!SOURCE_DIR1!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR2!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR3!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR4!\contract_address.txt"
        ) > "!ADDRESS_GET_FILE!"
    )

    :: Case 6: 16th directory gets the 12th to 15th contract_address.txt (separated by blank lines)
    if %%I EQU 16 (
        set "SOURCE_DIR1=!DIRS[12]!"
        set "SOURCE_DIR2=!DIRS[13]!"
        set "SOURCE_DIR3=!DIRS[14]!"
        set "SOURCE_DIR4=!DIRS[15]!"
        (
            type "%PARENT_DIR%\!SOURCE_DIR1!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR2!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR3!\contract_address.txt"
            type "%PARENT_DIR%\!SOURCE_DIR4!\contract_address.txt"
        ) > "!ADDRESS_GET_FILE!"
    )

    echo Created address_get.txt in !CURRENT_DIR!
)

echo ================================================
echo Address files generated successfully!
pause
