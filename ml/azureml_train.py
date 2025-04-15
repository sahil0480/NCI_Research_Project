from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment, Dataset
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.compute import AmlCompute, ComputeTarget
import os
import json

# Load credentials
with open(".azureml/config.json") as f:
    config = json.load(f)

svc_pr = ServicePrincipalAuthentication(
    tenant_id=config["tenantId"],
    service_principal_id=config["clientId"],
    service_principal_password=config["clientSecret"]
)

# Connect to workspace
ws = Workspace(
    subscription_id=config["subscriptionId"],
    resource_group=os.environ["AZURE_RESOURCE_GROUP"],
    workspace_name="nci-ml-workspace",
    auth=svc_pr
)

# Create experiment
experiment = Experiment(workspace=ws, name="cloud-performance-training")

# Create or get compute
compute_name = "cpu-cluster"
if compute_name in ws.compute_targets:
    compute_target = ws.compute_targets[compute_name]
else:
    compute_config = AmlCompute.provisioning_configuration(vm_size="STANDARD_DS11_V2", max_nodes=1)
    compute_target = ComputeTarget.create(ws, compute_name, compute_config)
    compute_target.wait_for_completion(show_output=True)

# Upload merged logs
datastore = ws.get_default_datastore()
datastore.upload(src_dir='logs', target_path='datasets', overwrite=True, show_progress=True)

# Define input dataset
dataset = Dataset.Tabular.from_delimited_files(path=(datastore, 'datasets/merged_logs.csv'))

# Prepare environment
env = Environment.from_conda_specification(name="train-env", file_path="env.yml")

# Script config
src = ScriptRunConfig(
    source_directory="ml",
    script="train_model.py",
    arguments=["--input-data", dataset.as_named_input('input').as_mount()],
    compute_target=compute_target,
    environment=env
)

# Submit & wait
run = experiment.submit(src)
run.wait_for_completion(show_output=True)

# Save best model info
metrics = run.get_metrics()
best_rmse = min(metrics.values())
best_model = min(metrics, key=metrics.get)
with open("ml/best_result.txt", "w") as f:
    f.write(f"{best_model},{best_rmse}")
