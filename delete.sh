for ctx in $(kubectl config get-contexts -o name); do
  echo "🧼 Cleaning up context: $ctx"
  
  # Delete all pods
  echo "⛔ Deleting all pods..."
  kubectl --context="$ctx" delete pods --all --ignore-not-found

  # Delete all PVCs normally
  echo "🗑️ Deleting PVCs..."
  kubectl --context="$ctx" delete pvc --all --ignore-not-found

  # Force delete stuck/terminating PVCs
  echo "🔥 Force deleting stuck PVCs (if any)..."
  stuck_pvcs=$(kubectl --context="$ctx" get pvc | grep Terminating | awk '{print $1}')
  for pvc in $stuck_pvcs; do
    echo "Force deleting PVC: $pvc"
    kubectl --context="$ctx" patch pvc "$pvc" -p '{"metadata":{"finalizers":null}}' --type=merge
  done

  echo "✅ Done with $ctx"
  echo "-----------------------------"
done

