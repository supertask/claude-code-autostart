# mac-setup

Mac起動時にClaude Codeの `--remote-control` セッションを5つ自動起動するアプリ。

## セットアップ

### 1. アプリをApplicationsにコピー

```bash
cp -r "Launch Claude Sessions.app" ~/Applications/
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

Terminal.appに5つのタブが開き、それぞれ `claude --remote-control` セッションが起動します。

## カスタマイズ

`Launch Claude Sessions.app/Contents/MacOS/launcher` を編集：

- `SESSION_COUNT=5` — セッション数
- `WORK_DIR="$HOME"` — 作業ディレクトリ

## ログイン項目の解除

システム設定 → 一般 → ログイン項目 から削除、またはコマンドで：

```bash
osascript -e 'tell application "System Events" to delete login item "Launch Claude Sessions"'
```
