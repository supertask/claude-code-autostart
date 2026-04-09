"""Claude Code セッション管理ロジック"""

import json
import os
import signal
import subprocess

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def _load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def _save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_session_count():
    return _load_config()["session_count"]


def set_session_count(count):
    config = _load_config()
    config["session_count"] = count
    _save_config(config)


def get_work_dir():
    return os.path.expanduser(_load_config()["work_dir"])


def get_running_pids():
    """claude --remote-control プロセスのPID一覧を返す"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "claude --remote-control"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return []
        return [int(pid) for pid in result.stdout.strip().split("\n") if pid]
    except Exception:
        return []


def get_status():
    pids = get_running_pids()
    return {
        "running": len(pids),
        "total": get_session_count(),
        "pids": pids,
    }


def start_all():
    """全セッションをTerminal.appで起動"""
    config = _load_config()
    count = config["session_count"]
    work_dir = os.path.expanduser(config["work_dir"])

    for _ in range(count):
        subprocess.run([
            "osascript", "-e",
            f'tell application "Terminal"\n'
            f'  activate\n'
            f'  do script "cd {work_dir} && claude --remote-control"\n'
            f'end tell'
        ])


def stop_all():
    """全セッションを停止してTerminalウィンドウを閉じる"""
    pids = get_running_pids()
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    # 空いたTerminalウィンドウを閉じる
    subprocess.run([
        "osascript", "-e",
        'tell application "Terminal"\n'
        '  set windowCount to count of windows\n'
        '  repeat with i from windowCount to 1 by -1\n'
        '    set w to window i\n'
        '    if busy of w is false then\n'
        '      close w\n'
        '    end if\n'
        '  end repeat\n'
        'end tell'
    ])


def restart_all():
    """全セッションを再起動"""
    stop_all()
    # プロセスが完全に終了するまで少し待つ
    import time
    time.sleep(2)
    start_all()
