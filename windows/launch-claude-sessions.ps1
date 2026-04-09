# Claude Code セッション自動起動スクリプト (Windows PowerShell)
# 5つの--remote-controlセッションをそれぞれ新しいウィンドウで起動する

$SessionCount = 5
$WorkDir = $env:USERPROFILE

for ($i = 1; $i -le $SessionCount; $i++) {
    Start-Process cmd -ArgumentList "/k", "cd /d $WorkDir && claude --remote-control `"Session $i`""
}
