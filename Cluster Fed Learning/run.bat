call Cluster1\run1.bat
call Cluster2\run2.bat
call Cluster3\run3.bat
call Cluster4\run4.bat
timeout /t 5 /nobreak
start cmd /k "python C1.py"
start cmd /k "python C2.py"
start cmd /k "python C3.py"
start cmd /k "python C4.py"
timeout /t 5 /nobreak
start cmd /k "python Server.py"