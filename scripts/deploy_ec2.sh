#!/bin/bash
set -e

# ==============================================================================
# AWS EC2 Continuous Deployment & eBPF Policy Sync Script
# ==============================================================================

EC2_USER=${1:-"ubuntu"}
EC2_HOST=${2:-"13.233.252.127"}
DOCKER_IMAGE=${3:-"ydurgadhanush/devsecops-pipeline:latest"}

echo "================================================="
echo " Deploying to AWS EC2: ${EC2_HOST}"
echo " Image: ${DOCKER_IMAGE}"
echo "================================================="

# Execute deployment commands on remote EC2 instance via SSH
ssh -o StrictHostKeyChecking=no "${EC2_USER}@${EC2_HOST}" << EOF
  set -e
  echo "[1/4] Pulling latest Docker image from registry..."
  sudo docker pull ${DOCKER_IMAGE}

  echo "[2/4] Stopping existing app container..."
  sudo docker stop devsecops-app || true
  sudo docker rm devsecops-app || true

  echo "[3/4] Launching updated container with resource bounds..."
  sudo docker run -d \
    --name devsecops-app \
    -p 80:5000 \
    --restart unless-stopped \
    ${DOCKER_IMAGE}

  echo "[4/4] Verifying local deployment status..."
  sleep 3
  curl -f http://localhost/health || exit 1
  echo "[✓] Deployment completed successfully on EC2!"
EOF