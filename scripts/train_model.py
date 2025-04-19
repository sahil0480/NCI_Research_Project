import pandas as pd
import joblib
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# 📥 Load the merged logs CSV
if len(sys.argv) < 2:
    print("Usage: train_model.py <csv_file>")
    sys.exit(1)

log_path = sys.argv[1]
df = pd.read_csv(log_path)

# 🧹 Preprocess: keep only successful entries
df = df[df["status"] == "success"]

# 💡 Feature & Label
# Map cloud to numeric classes
cloud_map = {"GCP": 0, "Azure": 1, "AWS": 2}
df["cloud_id"] = df["cloud"].map(cloud_map)

X = df[["duration_seconds"]]
y = df["cloud_id"]

# 🧪 Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 🧠 Define candidate models
models = {
    "logreg": LogisticRegression(),
    "rf": RandomForestClassifier(),
    "xgb": XGBClassifier(use_label_encoder=False, eval_metric="mlogloss"),
    "knn": KNeighborsClassifier()
}

# 🔍 Train + evaluate each
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    results[name] = (acc, model)

# 🏆 Pick the best
best_model_name = max(results, key=lambda k: results[k][0])
best_model = results[best_model_name][1]

# 💾 Save the model
joblib.dump(best_model, "model.pkl")

# 📊 Predict best cloud for most recent record
latest = df[["duration_seconds"]].tail(1)
predicted = best_model.predict(latest)[0]
reverse_map = {v: k for k, v in cloud_map.items()}

with open("best_cloud.txt", "w") as f:
    f.write(reverse_map[predicted])

print(f"✅ Trained model: {best_model_name}")
print(f"✅ Best cloud predicted: {reverse_map[predicted]}")
