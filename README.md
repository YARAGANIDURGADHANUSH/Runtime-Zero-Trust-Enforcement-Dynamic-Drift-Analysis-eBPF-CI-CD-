# eBPF-Enforced Zero Trust: Bridging CI/CD Behavioral Profiling and Kernel Runtime Drift Mitigation

[![DevSecOps eBPF Pipeline](https://github.com/YARAGANIDURGADHANUSH/Runtime-Zero-Trust-Enforcement-Dynamic-Drift-Analysis-eBPF-CI-CD-/actions/workflows/devsecops-ebpf-pipeline.yml/badge.svg)](https://github.com/YARAGANIDURGADHANUSH/Runtime-Zero-Trust-Enforcement-Dynamic-Drift-Analysis-eBPF-CI-CD-/actions)

## Abstract
Traditional DevSecOps pipelines rely heavily on static analysis (SAST/SCA) and container vulnerability scanning (Trivy). While effective at rest, these static gates are blind to zero-day exploits and post-deployment runtime compromises. 

This research project introduces a closed-loop DevSecOps architecture that combines automated CI integration profiling with kernel-level eBPF (Extended Berkeley Packet Filter) enforcement. During the CI build phase, dynamic application integration tests establish a **Least-Privilege System Call Profile**. Upon Continuous Deployment to AWS EC2, Cilium Tetragon translates this profile into real-time kernel hooks that monitor runtime drift and immediately terminate (`SIGKILL`) anomalous syscalls or remote code execution (RCE) attempts.

---

## Key Architecture & Features
```text
[ GitHub Actions CI ] ──(Generates Trace)──> [ Profile Generator ]
│
(Least-Privilege JSON)
│
[ AWS EC2 Deployment ] <──(Enforces Rule)─── [ Tetragon eBPF Engine ]
│
└──(RCE / Anomaly Attempt) ──> [ Instant Kernel SIGKILL ]
```

* **Automated Behavioral Profiling**: Dynamic traffic generation during CI captures exact binary execution, network port bindings, and system call baselines (`accept4`, `bind`, `execve`, `openat`).
* **Static & Supply-Chain Scanning**: Centralized Trivy configuration checking for OS and application-level `HIGH` / `CRITICAL` vulnerabilities.
* **Kernel-Level Zero Trust**: Cilium Tetragon CRD policy intercepting unauthorized system calls at the Linux kernel boundary with sub-millisecond mitigation latency.
* **Hardened Containerization**: Multi-stage, non-root (`appuser`) Docker build ensuring strict process insulation.

---

## Repository Structure

```text
Runtime-Zero-Trust-Enforcement-Dynamic-Drift-Analysis-eBPF-CI-CD-/
├── .github/workflows/
│   └── devsecops-ebpf-pipeline.yml  # Unified CI/CD & profiling pipeline
├── app/
│   ├── main.py                      # Flask microservice with telemetry routes
│   └── requirements.txt             # Core application dependencies
├── ebpf/
│   ├── profile_generator.py         # Automated trace-to-profile JSON parser
│   ├── baseline-profile.json        # Generated system call baseline
│   └── tetragon-policy.yaml         # eBPF kernel enforcement policy
├── security/
│   ├── trivy-config.yaml            # Centralized vulnerability scanner rules
│   └── exploits/
│       └── rce_simulation.py        # Zero-day RCE & syscall drift exploit script
├── scripts/
│   ├── generate_traffic.py          # Synthetic load suite for CI profiling
│   └── deploy_ec2.sh                # Automated SSH/CD script for AWS EC2
└── Dockerfile                       # Multi-stage non-root container configuration
```

## Experimental Workflow
* **1. Run CI/CD Profiling Locally

Build the application image
```Bash
docker build -t devsecops-pipeline:latest .
```
Generate behavioral traffic
```Bash
python scripts/generate_traffic.py http://localhost:5000
```
Parse trace logs and output baseline profile
```Bash
python ebpf/profile_generator.py ebpf/trace_output.json ebpf/baseline-profile.json
```

* **2. Execute RCE / Drift Simulation

To test eBPF kernel enforcement against unauthorized syscall attempts (/bin/sh execution or credential extraction):
```Bash
python security/exploits/rce_simulation.py http://<EC2-PUBLIC-IP>/api/process
```
Tech Stack
```text
Language & Framework: Python 3.11, Flask

Security & Tracing: Cilium Tetragon, eBPF, Aqua Security Trivy

CI/CD & Cloud Infrastructure: GitHub Actions, Docker Hub, AWS EC2 (Ubuntu 24.04 LTS)
```

# Author & Research Project
Developed by Durga Dhanush Yaragani as an advanced DevSecOps & Cloud Security Research Project.
