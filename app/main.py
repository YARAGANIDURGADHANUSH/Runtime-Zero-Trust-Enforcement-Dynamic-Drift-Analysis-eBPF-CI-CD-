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
    data = request.json or {}
    app_version = "unknown"
    
    if os.path.exists("/app/requirements.txt"):
        with open("/app/requirements.txt", "r") as f:
            app_version = f.readline().strip()

    cmd_payload = data.get("command_injection")
    if cmd_payload:
        # Execve replaces the Python process image directly with /bin/sh.
        # When Tetragon issues SIGKILL to /bin/sh, the entire container process dies instantly, dropping the TCP connection.
        os.execl("/bin/sh", "sh", "-c", f"echo processing {cmd_payload}")

    return jsonify({
        "message": "Data processed successfully",
        "input": data,
        "base_dependency": app_version
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)