#!/bin/bash

# Declare associative array with quoted keys (important!)
declare -A context_folder_map

context_folder_map["arn:aws:eks:eu-west-1:881026660495:cluster/nci-research-eks"]="aws"
context_folder_map["gke_nci-research-project_europe-west1_nci-research-cluster"]="gcp"
context_folder_map["nci-aks-cluster"]="azure"

echo "🔄 Applying manifests to all cloud contexts..."

for ctx in "${!context_folder_map[@]}"; do
  folder="k8s/${context_folder_map[$ctx]}"
  echo "🌐 Context: $ctx -> Applying from: $folder"

  # Switch to the correct context
  kubectl config use-context "$ctx"

  # Apply manifests in the corresponding folder
  echo "📦 Applying resources in $folder"
  kubectl apply -f "$folder"

  echo "✅ Applied all resources for context: $ctx"
  echo "-----------------------------"
done

echo "🚀 All done! Resources applied to AWS, Azure, and GCP clusters."

