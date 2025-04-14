#!/bin/bash

# reset.sh - Force delete all K8s resources from AWS, Azure, GCP contexts.

set -e

contexts=(
  "arn:aws:eks:eu-west-1:881026660495:cluster/nci-research-eks"
  "nci-aks-cluster"
  "gke_nci-research-project_europe-west1_nci-research-cluster"
)

echo "🧹 Starting full cleanup..."

for ctx in "${contexts[@]}"; do
  echo "🔁 Switching context to: $ctx"
  kubectl config use-context "$ctx"

  echo "⛔ Deleting all deployments, services, and pods..."
  kubectl delete deployments --all --ignore-not-found
  kubectl delete svc --all --ignore-not-found
  kubectl delete pods --all --ignore-not-found

  echo "🧨 Force deleting stuck PVCs..."
  stuck_pvcs=$(kubectl get pvc -o json | jq -r '.items[] | select(.metadata.finalizers) | .metadata.name')
  for pvc in $stuck_pvcs; do
    kubectl patch pvc "$pvc" -p '{"metadata":{"finalizers":null}}' --type=merge
  done

  kubectl delete pvc --all --ignore-not-found

  echo "✅ Cleaned up cluster: $ctx"
  echo "---------------------------------------"
done

echo "✅ All contexts cleaned!"
