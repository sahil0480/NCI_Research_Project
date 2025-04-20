import pandas as pd
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

# Validate input
if len(sys.argv) != 2:
    print("Usage: python train_model.py merged_logs.csv")
    sys.exit(1)

# Read CSV safely
csv_path = sys.argv[1]
df = pd.read_csv(csv_path, on_bad_lines='skip')

# Filter and clean data
df = df.dropna()
df = df[df['status'] == 'success']  # Use only successful deploys

# Encode cloud provider as integer
le = LabelEncoder()
df['cloud_encoded'] = le.fit_transform(df['cloud'])  # GCP, Azure, AWS -> 0,1,2

# Define features and target
X = df[['duration_seconds']]
y = df['cloud_encoded']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model candidates
models = {
    'LogisticRegression': LogisticRegression(),
    'RandomForest': RandomForestClassifier(),
    'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    'KNN': KNeighborsClassifier()
}

# Training loop
best_model = None
best_acc = 0
best_model_name = ""

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"{name} accuracy: {acc:.4f}")

    if acc > best_acc:
        best_acc = acc
        best_model = model
        best_model_name = name

# Save best model
joblib.dump(best_model, "model.pkl")
print(f"✅ Best model: {best_model_name} (Accuracy: {best_acc:.4f})")

# Predict best cloud from most recent deployment
latest = df.sort_values(by='end_time', ascending=False).iloc[0]
predicted_class = best_model.predict([[latest['duration_seconds']]])[0]
best_cloud = le.inverse_transform([predicted_class])[0]

# Save to file
with open("best_cloud.txt", "w") as f:
    f.write(best_cloud)

print(f"🚀 Best cloud selected: {best_cloud}")
