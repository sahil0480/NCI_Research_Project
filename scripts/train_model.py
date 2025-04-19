import pandas as pd
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegressio
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

# Load CSV file
if len(sys.argv) != 2:
    print("Usage: python train_model.py merged_logs.csv")
    sys.exit(1)

df = pd.read_csv(sys.argv[1])

# Preprocess
df = df.dropna()
df = df[df['status'] == 'success']  # Filter only successful deploys

# Encode cloud as label
le = LabelEncoder()
df['cloud_encoded'] = le.fit_transform(df['cloud'])  # GCP, Azure, AWS -> 0,1,2

# Features and target
X = df[['duration_seconds']]
y = df['cloud_encoded']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models
models = {
    'LogisticRegression': LogisticRegression(),
    'RandomForest': RandomForestClassifier(),
    'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    'KNN': KNeighborsClassifier()
}

best_model = None
best_acc = 0
best_model_name = ""
best_model_file = "model.pkl"

# Train and evaluate
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
joblib.dump(best_model, best_model_file)
print(f"Best model: {best_model_name} (Accuracy: {best_acc:.4f})")

# Predict best cloud from most recent deployment
latest = df.sort_values(by='end_time', ascending=False).iloc[0]
predicted_class = best_model.predict([[latest['duration_seconds']]])[0]
best_cloud = le.inverse_transform([predicted_class])[0]

# Save the best cloud
with open("best_cloud.txt", "w") as f:
    f.write(best_cloud)

print(f"Best cloud selected: {best_cloud}")
