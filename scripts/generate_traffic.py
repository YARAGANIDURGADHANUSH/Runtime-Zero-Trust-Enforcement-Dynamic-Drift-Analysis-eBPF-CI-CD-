import requests
import time
import sys

BASE_URL = "http://localhost:5000"

def generate_baseline_traffic(target_url):
    """
    Exercises all benign endpoints during CI integration testing to generate 
    a complete eBPF syscall trace baseline.
    """
    print(f"[*] Starting synthetic traffic generation against: {target_url}")
    endpoints = [
        {"method": "GET", "path": "/"},
        {"method": "GET", "path": "/health"},
        {"method": "POST", "path": "/api/process", "payload": {"user": "ci_runner", "action": "profile"}},
        {"method": "POST", "path": "/api/process", "payload": {"batch_id": 101, "items": [1, 2, 3]}}
    ]

    for attempt in range(10):
        try:
            res = requests.get(f"{target_url}/health", timeout=2)
            if res.status_code == 200:
                print("[✓] Target container is online. Dispatching traffic suite...")
                break
        except requests.exceptions.RequestException:
            print(f"[!] Target not ready yet. Retrying ({attempt + 1}/10)...")
            time.sleep(2)
    else:
        print("[X] Container health check failed. Aborting traffic generation.")
        sys.exit(1)

    # Execute benign routes to capture normal operational syscalls
    for ep in endpoints:
        try:
            if ep["method"] == "GET":
                response = requests.get(f"{target_url}{ep['path']}")
            elif ep["method"] == "POST":
                response = requests.post(f"{target_url}{ep['path']}", json=ep.get("payload", {}))
            
            print(f"[✓] Executed {ep['method']} {ep['path']} -> Status: {response.status_code}")
        except Exception as e:
            print(f"[X] Error requesting {ep['path']}: {e}")
        time.sleep(0.5)

    print("[✓] Behavioral profiling traffic successfully completed.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    generate_baseline_traffic(target)