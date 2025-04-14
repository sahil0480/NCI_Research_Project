import os
import glob
import shutil
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
import xgboost as xgb

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    print("⚠️ LightGBM not installed. Skipping that model.")
    LIGHTGBM_AVAILABLE = False

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def download_logs():
    print("📥 Downloading logs from all clouds...")

    if shutil.which("gsutil"):
        try:
            subprocess.run(["gsutil", "cp", "gs://nci-deployment-logs/deploy-log-gcp-*.csv", "logs/"], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ GCP logs not found or gsutil failed.")
    else:
        print("❌ gsutil not found.")

    if shutil.which("az"):
        try:
            subprocess.run([
                "az", "storage", "blob", "download-batch",
                "--account-name", os.environ["AZURE_STORAGE_ACCOUNT"],
                "--destination", "logs",
                "--source", os.environ["AZURE_LOG_CONTAINER"],
                "--pattern", "deploy-log-azure-*.csv",
                "--account-key", os.environ["AZURE_STORAGE_KEY"]
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ Azure logs not found or az CLI failed.")
    else:
        print("❌ Azure CLI not found.")

    if shutil.which("aws"):
        try:
            subprocess.run([
                "aws", "s3", "cp", f"s3://{os.environ['AWS_LOG_BUCKET']}/", "logs/",
                "--recursive", "--exclude", "*", "--include", "deploy-log-aws-*.csv"
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ AWS logs not found or AWS CLI failed.")
    else:
        print("❌ AWS CLI not found.")

def load_logs():
    print("📊 Loading logs...")
    dfs = []
    for file in glob.glob("logs/deploy-log-*.csv"):
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"✅ Loaded: {file}")
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
    return dfs

def preprocess(df):
    print("🧹 Preprocessing...")
    df = df.dropna()
    df["duration_seconds"] = df["duration_seconds"].astype(float)
    df["cpu_usage_millicores"] = pd.to_numeric(df["cpu_usage_millicores"], errors='coerce').fillna(0)
    df["mem_usage_mib"] = pd.to_numeric(df["mem_usage_mib"], errors='coerce').fillna(0)
    df["pod_count"] = pd.to_numeric(df["pod_count"], errors='coerce').fillna(0)
    df = df.dropna()
    return df

def train_models(X_train, X_test, y_train, y_test):
    results = {}

    models = {
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Ridge": Ridge(),
        "XGBoost": xgb.XGBRegressor(n_estimators=100, random_state=42)
    }

    if LIGHTGBM_AVAILABLE:
        models["LightGBM"] = lgb.LGBMRegressor(n_estimators=100, random_state=42)

    for name, model in models.items():
        print(f"🚀 Training: {name}")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = mean_squared_error(y_test, preds, squared=False)
        results[name] = rmse
        print(f"✅ {name} RMSE: {rmse:.2f}")

    return results

def plot_results(results):
    print("📊 Plotting model comparison...")
    plt.figure(figsize=(8, 5))
    plt.bar(results.keys(), results.values(), color="skyblue")
    plt.ylabel("RMSE")
    plt.title("Model Comparison - Lower RMSE is Better")
    plt.tight_layout()
    plt.savefig("logs/model_rmse_comparison.png")
    print("📈 Saved: logs/model_rmse_comparison.png")

def main():
    download_logs()
    dfs = load_logs()
    if not dfs:
        print("❌ No logs found. Exiting.")
        return

    combined = pd.concat(dfs, ignore_index=True)
    df = preprocess(combined)

    features = ["pod_count", "cpu_usage_millicores", "mem_usage_mib"]
    target = "duration_seconds"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    results = train_models(X_train, X_test, y_train, y_test)
    plot_results(results)

    # Determine best model
    best_model = min(results, key=results.get)
    print(f"🏆 Best Model: {best_model} with RMSE = {results[best_model]:.2f}")

    # Save best model name
    with open("logs/best_model.txt", "w") as f:
        f.write(best_model)

    # Save processed logs
    df.to_csv("logs/processed_logs.csv", index=False)
    print("✅ Saved processed dataset to logs/processed_logs.csv")

if __name__ == "__main__":
    main()
