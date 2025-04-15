import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input-data", type=str, required=True)
args = parser.parse_args()

print("📥 Reading merged logs CSV from:", args.input_data)
df = pd.read_csv(os.path.join(args.input_data, "merged_logs.csv"))

# Proceed with training...
print("🔍 Dataset preview:\n", df.head())
