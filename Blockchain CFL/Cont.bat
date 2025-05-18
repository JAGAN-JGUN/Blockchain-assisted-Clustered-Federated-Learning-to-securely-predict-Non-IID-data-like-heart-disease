@echo off
setlocal enabledelayedexpansion

set "PARENT_DIR=%CD%"

echo Starting Truffle migrations in all workspaces...
echo ================================================

for /D %%D in (*) do (
    echo.
    echo Migrating in workspace: %%D
    cd %%D

    call truffle migrate --reset > migrate_output.txt 2>&1

    if exist migrate_output.txt (
        for /f "tokens=4" %%A in ('findstr /C:"contract address:" migrate_output.txt') do (
            echo %%A > contract_address.txt
            echo Contract address saved in %%D\contract_address.txt
        )
        del migrate_output.txt
    ) else (
        echo Migration failed or output file not created in %%D
    )
    cd "%PARENT_DIR%"
)

echo ================================================
echo Migration process completed for all workspaces.
pause
