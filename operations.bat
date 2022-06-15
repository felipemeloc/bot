@echo off
set LOGFILE="C:\Users\FelipeMelo\Soter Professional Services\Soter Data Analysts - bot_project\bot\logs\operations_batch.log"
call :LOG > %LOGFILE%
exit /B

:LOG
python "C:\Users\FelipeMelo\Soter Professional Services\Soter Data Analysts - bot_project\bot\sales.py" %*