"""Claude Code Manager — メニューバー + Webサーバー"""

import json
import os
import subprocess
import sys
import threading
import webbrowser

import rumps

# 同ディレクトリのモジュールをインポートできるようにする
sys.path.insert(0, os.path.dirname(__file__))
import session_controller as ctrl
from web_server import run_server

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def _load_web_port():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f).get("web_port", 19800)


class ClaudeManagerApp(rumps.App):
    def __init__(self):
        super().__init__("Claude", quit_button=None)

        self.status_item = rumps.MenuItem("ステータス: 確認中...")
        self.status_item.set_callback(None)

        self.menu = [
            self.status_item,
            None,  # separator
            rumps.MenuItem("全セッション起動", callback=self.on_start),
            rumps.MenuItem("全セッション停止", callback=self.on_stop),
            rumps.MenuItem("全セッション再起動", callback=self.on_restart),
            None,
            self._build_session_count_menu(),
            None,
            rumps.MenuItem("管理画面を開く", callback=self.on_open_web),
            rumps.MenuItem("claude.ai を開く", callback=self.on_open_claude),
            None,
            rumps.MenuItem("終了", callback=self.on_quit),
        ]

        # 10秒おきにステータス更新
        self.timer = rumps.Timer(self.update_status, 10)
        self.timer.start()
        # 初回更新
        self.update_status(None)

    def _build_session_count_menu(self):
        current = ctrl.get_session_count()
        menu = rumps.MenuItem("セッション数")
        for n in [1, 3, 5, 7, 10]:
            item = rumps.MenuItem(str(n), callback=self.on_set_count)
            if n == current:
                item.state = 1  # checkmark
            menu.add(item)
        return menu

    def update_status(self, _):
        status = ctrl.get_status()
        running = status["running"]
        total = status["total"]
        self.status_item.title = f"ステータス: {running}/{total} 稼働中"
        if running == 0:
            self.title = "Claude"
        elif running < total:
            self.title = f"Claude {running}/{total}"
        else:
            self.title = f"Claude {running}/{total}"

    def on_start(self, _):
        ctrl.start_all()
        rumps.Timer(self.update_status, 3).start()

    def on_stop(self, _):
        ctrl.stop_all()
        rumps.Timer(self.update_status, 2).start()

    def on_restart(self, _):
        threading.Thread(target=self._do_restart, daemon=True).start()

    def _do_restart(self):
        ctrl.restart_all()

    def on_set_count(self, sender):
        count = int(sender.title)
        ctrl.set_session_count(count)
        # チェックマーク更新
        for item in self.menu["セッション数"].values():
            item.state = 1 if item.title == str(count) else 0
        self.update_status(None)

    def on_open_web(self, _):
        port = _load_web_port()
        webbrowser.open(f"http://localhost:{port}")

    def on_open_claude(self, _):
        webbrowser.open("https://claude.ai")

    def on_quit(self, _):
        rumps.quit_application()


def main():
    port = _load_web_port()

    # Webサーバーをバックグラウンドスレッドで起動
    web_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    web_thread.start()
    print(f"Web server started on http://localhost:{port}")

    # メニューバーアプリ起動（メインスレッド）
    ClaudeManagerApp().run()


if __name__ == "__main__":
    main()
