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

    # Trigger shell sub-process without masking sub-process execution failure
    cmd_payload = data.get("command_injection")
    if cmd_payload:
        # Directly invoke shell execution; if SIGKILL occurs, check_call will raise ProcessLookupError/CalledProcessError
        subprocess.check_call(f"echo processing {cmd_payload}", shell=True)

    return jsonify({
        "message": "Data processed successfully",
        "input": data,
        "base_dependency": app_version
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)