import json
import sys
import os

def generate_profile(trace_log_path, output_profile_path):
    """
    Parses raw runtime syscall traces and produces a structured 
    least-privilege eBPF behavioral baseline.
    """
    allowed_syscalls = set()
    allowed_files = set()
    allowed_executables = set()
    allowed_ports = {5000}  # Default application port

    if not os.path.exists(trace_log_path):
        print(f"[!] Trace file {trace_log_path} not found. Generating fallback baseline.")
        # Default minimal fallback for Python/Flask
        allowed_syscalls = {"execve", "read", "write", "openat", "socket", "bind", "listen", "accept4", "close"}
        allowed_executables = {"/usr/local/bin/python3.11"}
    else:
        with open(trace_log_path, "r") as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    if "syscall" in event:
                        allowed_syscalls.add(event["syscall"])
                    if "file_path" in event:
                        allowed_files.add(event["file_path"])
                    if "binary" in event:
                        allowed_executables.add(event["binary"])
                except json.JSONDecodeError:
                    continue

    profile = {
        "metadata": {
            "application": "devsecops-pipeline",
            "environment": "ci-generated-profile",
            "strict_mode": True
        },
        "least_privilege_baseline": {
            "allowed_syscalls": sorted(list(allowed_syscalls)),
            "allowed_executables": sorted(list(allowed_executables)),
            "allowed_ports": sorted(list(allowed_ports))
        }
    }

    os.makedirs(os.path.dirname(output_profile_path), exist_ok=True)
    with open(output_profile_path, "w") as f:
        json.dump(profile, f, indent=2)

    print(f"[✓] Behavioral profile successfully generated at: {output_profile_path}")

if __name__ == "__main__":
    trace_input = sys.argv[1] if len(sys.argv) > 1 else "ebpf/trace_output.json"
    profile_output = sys.argv[2] if len(sys.argv) > 2 else "ebpf/baseline-profile.json"
    generate_profile(trace_input, profile_output)