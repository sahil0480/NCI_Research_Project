#!/bin/bash

# List of contexts
CONTEXTS=(
  "arn:aws:eks:eu-west-1:881026660495:cluster/nci-research-eks"
  "nci-aks-cluster"
  "gke_nci-research-project_europe-west1_nci-research-cluster"
)

for CONTEXT in "${CONTEXTS[@]}"; do
  echo "🌀 Switching to context: $CONTEXT"
  kubectl config use-context "$CONTEXT"

  echo "🔥 Deleting all pods (forcefully)..."
  kubectl delete pods --all --grace-period=0 --force

  echo "🧹 Deleting all PVCs (handling stuck ones)..."
  for pvc in $(kubectl get pvc --no-headers | awk '{print $1}'); do
    echo "➡️ Patching and deleting PVC: $pvc"
    kubectl patch pvc "$pvc" -p '{"metadata":{"finalizers":null}}' --type=merge
    kubectl delete pvc "$pvc" --grace-period=0 --force
  done

  echo "✅ Cleanup done for: $CONTEXT"
  echo "-------------------------------"
done

echo "🎉 Multi-cloud cleanup complete!"
