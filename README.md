# claude-code-autostart

Mac/Windows起動時にClaude Codeの `--remote-control` セッションを5つ自動起動する。

## 構成

```
├── mac/
│   ├── Launch Claude Sessions.app/   # .appバンドル（ログイン項目に登録）
│   └── launch-claude-sessions.sh     # 単体スクリプト版
└── windows/
    ├── launch-claude-sessions.bat    # バッチファイル版
    └── launch-claude-sessions.ps1   # PowerShell版
```

## Mac セットアップ

### 1. アプリをApplicationsにコピー

```bash
cp -r mac/Launch\ Claude\ Sessions.app ~/Applications/
chmod +x ~/Applications/Launch\ Claude\ Sessions.app/Contents/MacOS/launcher
```

### 2. ログイン項目に登録

```bash
osascript -e 'tell application "System Events" to make login item at end with properties {path:"'$HOME'/Applications/Launch Claude Sessions.app", hidden:false}'
```

### 3. 動作確認

```bash
open ~/Applications/Launch\ Claude\ Sessions.app
```

## Windows セットアップ

### 1. スタートアップフォルダにコピー

```powershell
Copy-Item windows\launch-claude-sessions.bat "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\"
```

### 2. 動作確認

```powershell
.\windows\launch-claude-sessions.bat
```

## カスタマイズ

各スクリプト内の以下を編集：

- `SESSION_COUNT` — セッション数（デフォルト: 5）
- `WORK_DIR` — 作業ディレクトリ（デフォルト: ホームディレクトリ）

## ログイン項目の解除

**Mac**: システム設定 → 一般 → ログイン項目 から削除

**Windows**: スタートアップフォルダから `.bat` ファイルを削除
