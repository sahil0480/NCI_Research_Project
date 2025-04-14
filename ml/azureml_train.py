from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.compute import AmlCompute, ComputeTarget
import os

# Connect to Azure ML Workspace
ws = Workspace.from_config(path="azureml_config.json")  # Create this config file in GitHub Secrets or workspace
experiment = Experiment(workspace=ws, name="cloud-performance-training")

# Attach compute
compute_name = "cpu-cluster"
if compute_name in ws.compute_targets:
    compute_target = ws.compute_targets[compute_name]
else:
    compute_config = AmlCompute.provisioning_configuration(vm_size="STANDARD_DS11_V2", max_nodes=1)
    compute_target = ComputeTarget.create(ws, compute_name, compute_config)
    compute_target.wait_for_completion(show_output=True)

# Set environment
env = Environment.from_conda_specification(name="train-env", file_path="env.yml")

# Run training script
src = ScriptRunConfig(source_directory=".", 
                      script="train_model.py", 
                      compute_target=compute_target,
                      environment=env)

run = experiment.submit(src)
run.wait_for_completion(show_output=True)

# Save metrics to a file for GitHub Action
metrics = run.get_metrics()
best_rmse = min(metrics.values())
best_model = min(metrics, key=metrics.get)

with open("best_result.txt", "w") as f:
    f.write(f"{best_model},{best_rmse}")
