from flask import Flask, jsonify, request
import os
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "eBPF-Monitored Microservice",
        "version": "2.0.0"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/process", methods=["POST"])
def process_data():
    """Simulates business logic with dynamic sub-shell execution for eBPF profiling."""
    data = request.json or {}
    app_version = "unknown"
    
    if os.path.exists("/app/requirements.txt"):
        with open("/app/requirements.txt", "r") as f:
            app_version = f.readline().strip()

    # Trigger shell sub-process to fire sys_enter_execve kernel events
    cmd_payload = data.get("command_injection")
    if cmd_payload:
        try:
            subprocess.run(f"echo processing {cmd_payload}", shell=True, timeout=2, capture_output=True)
        except Exception:
            pass

    return jsonify({
        "message": "Data processed successfully",
        "input": data,
        "base_dependency": app_version
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)