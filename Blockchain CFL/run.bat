@echo off
setlocal enabledelayedexpansion

for /D %%d in (*) do (
    if exist "%%d\deploy.py" (
        echo Running deploy.py in %%d
        pushd "%%d"
        python deploy.py
        popd
    )
)

echo All deployments finished.
pause