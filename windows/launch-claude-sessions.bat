@echo off
REM Claude Code セッション自動起動スクリプト (Windows)
REM 5つの--remote-controlセッションをそれぞれ新しいウィンドウで起動する

set SESSION_COUNT=5
set WORK_DIR=%USERPROFILE%

for /L %%i in (1,1,%SESSION_COUNT%) do (
    start "Claude Session %%i" cmd /k "cd /d %WORK_DIR% && claude --remote-control --trust-workspace"
)
