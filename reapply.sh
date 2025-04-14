#!/bin/bash

# reapply.sh - Reapply Kubernetes manifests for all cloud clusters.

set -e

contexts=(
  "arn:aws:eks:eu-west-1:881026660495:cluster/nci-research-eks"
  "nci-aks-cluster"
  "gke_nci-research-project_europe-west1_nci-research-cluster"
)

echo "📦 Starting deployment for all cloud contexts..."

for ctx in "${contexts[@]}"; do
  echo "🔄 Switching context to: $ctx"
  kubectl config use-context "$ctx"

  if [[ "$ctx" == *"eks"* ]]; then
    folder="aws"
  elif [[ "$ctx" == *"aks"* ]]; then
    folder="azure"
  else
    folder="gcp"
  fi

  echo "📁 Applying manifests in k8s/$folder"
  kubectl apply -f "k8s/$folder/"
  echo "✅ Applied manifests to $ctx"
  echo "---------------------------------------"
done

echo "🚀 All cloud deployments complete!"
