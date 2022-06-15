@echo off
set LOGFILE="C:\Users\FelipeMelo\Soter Professional Services\Soter Data Analysts - bot_project\telegram_report_bot\logs\locksmiths_batch.log"
call :LOG > %LOGFILE%
exit /B

:LOG
python "C:\Users\FelipeMelo\Soter Professional Services\Soter Data Analysts - bot_project\telegram_report_bot\locksmiths.py" %*