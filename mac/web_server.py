"""Flask Webサーバー + API"""

from flask import Flask, jsonify, render_template, request
import session_controller as ctrl

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def api_status():
    return jsonify(ctrl.get_status())


@app.route("/api/start", methods=["POST"])
def api_start():
    ctrl.start_all()
    return jsonify({"ok": True, "action": "start"})


@app.route("/api/stop", methods=["POST"])
def api_stop():
    ctrl.stop_all()
    return jsonify({"ok": True, "action": "stop"})


@app.route("/api/restart", methods=["POST"])
def api_restart():
    ctrl.restart_all()
    return jsonify({"ok": True, "action": "restart"})


@app.route("/api/config", methods=["GET"])
def api_get_config():
    return jsonify({
        "session_count": ctrl.get_session_count(),
        "work_dir": ctrl.get_work_dir(),
    })


@app.route("/api/config", methods=["POST"])
def api_set_config():
    data = request.get_json()
    if "session_count" in data:
        ctrl.set_session_count(int(data["session_count"]))
    return jsonify({"ok": True})


def run_server(port=19800):
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
