# claude-code-autostart

Mac/Windows起動時にClaude Codeの `--remote-control` セッションを管理するツール。

## Mac: Claude Code Manager

メニューバー常駐アプリ + Web管理画面でセッションを制御。

### セットアップ

```bash
cd mac
pip3 install -r requirements.txt
```

### 起動

```bash
cd mac
python3 claude_manager.py
```

メニューバーに「Claude」が表示され、`http://localhost:19800` でWeb管理画面にアクセスできます。

### 機能

- **メニューバー**: 全起動/全停止/再起動、セッション数変更、ステータス表示
- **Web管理画面**: ブラウザから同じ操作（Tailscale経由でリモートからも）
- **API**: `GET /api/status`, `POST /api/start`, `POST /api/stop`, `POST /api/restart`, `GET/POST /api/config`

### ログイン項目に登録（Mac起動時に自動起動）

```bash
cp -r mac/Launch\ Claude\ Sessions.app ~/Applications/
chmod +x ~/Applications/Launch\ Claude\ Sessions.app/Contents/MacOS/launcher
osascript -e 'tell application "System Events" to make login item at end with properties {path:"'$HOME'/Applications/Launch Claude Sessions.app", hidden:false}'
```

### カスタマイズ

`mac/config.json` を編集：

```json
{
  "session_count": 5,
  "work_dir": "~",
  "web_port": 19800
}
```

## Windows

シンプルなスクリプト版（GUI管理は今後対応予定）。

### 起動

```powershell
.\windows\launch-claude-sessions.bat
```

### スタートアップ登録

```powershell
Copy-Item windows\launch-claude-sessions.bat "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\"
```

## ログイン項目の解除

**Mac**: システム設定 → 一般 → ログイン項目 から削除

**Windows**: スタートアップフォルダから `.bat` ファイルを削除
