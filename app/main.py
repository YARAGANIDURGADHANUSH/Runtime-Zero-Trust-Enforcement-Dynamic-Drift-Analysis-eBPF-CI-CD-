from flask import Flask, jsonify, request
import os
import urllib.request

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
    """Simulates internal business logic and file reading for profiling."""
    data = request.json or {}
    # Simulate a controlled file read operation
    app_version = "unknown"
    if os.path.exists("/app/requirements.txt"):
        with open("/app/requirements.txt", "r") as f:
            app_version = f.readline().strip()
            
    return jsonify({
        "message": "Data processed successfully",
        "input": data,
        "base_dependency": app_version
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)