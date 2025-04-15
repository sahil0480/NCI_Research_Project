from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.authentication import ServicePrincipalAuthentication
import os
import json

# Load credentials from secret
with open(".azureml/config.json") as f:
    config = json.load(f)

svc_pr = ServicePrincipalAuthentication(
    tenant_id=config["tenantId"],
    service_principal_id=config["clientId"],
    service_principal_password=config["clientSecret"]
)

ws = Workspace(
    subscription_id=config["subscriptionId"],
    resource_group=os.environ["AZURE_RESOURCE_GROUP"],
    workspace_name="model_training",
    auth=svc_pr
)

experiment = Experiment(workspace=ws, name="cloud-performance-training")

# Attach compute
from azureml.core.compute import AmlCompute, ComputeTarget

compute_name = "cpu-cluster"
if compute_name in ws.compute_targets:
    compute_target = ws.compute_targets[compute_name]
else:
    compute_config = AmlCompute.provisioning_configuration(vm_size="STANDARD_DS11_V2", max_nodes=1)
    compute_target = ComputeTarget.create(ws, compute_name, compute_config)
    compute_target.wait_for_completion(show_output=True)

# Create/run experiment
env = Environment.from_conda_specification(name="train-env", file_path="env.yml")
src = ScriptRunConfig(source_directory=".", script="train_model.py", compute_target=compute_target, environment=env)
run = experiment.submit(src)
run.wait_for_completion(show_output=True)

# Save best model
metrics = run.get_metrics()
best_rmse = min(metrics.values())
best_model = min(metrics, key=metrics.get)
with open("best_result.txt", "w") as f:
    f.write(f"{best_model},{best_rmse}")
