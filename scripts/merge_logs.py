import os
import pandas as pd

LOG_DIR = "logs"
OUTPUT_FILE = os.path.join(LOG_DIR, "merged_logs.csv")

def is_valid_log(file_name):
    return file_name.endswith(".csv") and file_name.startswith("deploy-log")

def main():
    log_files = [f for f in os.listdir(LOG_DIR) if is_valid_log(f)]
    if not log_files:
        print("❌ No log files found to merge.")
        exit(1)

    merged_df = pd.DataFrame()
    for file in log_files:
        path = os.path.join(LOG_DIR, file)
        try:
            df = pd.read_csv(path)
            merged_df = pd.concat([merged_df, df], ignore_index=True)
        except Exception as e:
            print(f"⚠️ Failed to read {file}: {e}")

    if merged_df.empty:
        print("❌ Merged dataframe is empty. No logs processed.")
        exit(1)

    merged_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Merged {len(log_files)} files into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
