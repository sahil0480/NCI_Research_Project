import sys
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

def load_data(filepath):
    df = pd.read_csv(filepath)
    df = df[df['status'] == 'success']
    df = df.drop(columns=['status'])

    # Feature Engineering
    df['start_time'] = pd.to_numeric(df['start_time'], errors='coerce')
    df['end_time'] = pd.to_numeric(df['end_time'], errors='coerce')
    df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
    df = df.dropna()

    # Encode cloud as target
    df['cloud'] = df['cloud'].astype('category').cat.codes
    return df

def train_and_select_best(X_train, y_train, X_test, y_test):
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
        'GradientBoosting': GradientBoostingClassifier(),
        'LogisticRegression': LogisticRegression(max_iter=500)
    }

    best_model = None
    best_score = 0
    best_name = ""

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"{name} accuracy: {acc:.4f}")

        if acc > best_score:
            best_model = model
            best_score = acc
            best_name = name

    print(f"\n✔️ Best model: {best_name} (Accuracy: {best_score:.4f})")
    return best_model

def save_outputs(model, best_cloud_index, label_map):
    joblib.dump(model, "model.pkl")
    best_cloud = label_map[best_cloud_index]
    with open("best_cloud.txt", "w") as f:
        f.write(best_cloud)
    print(f"✅ Predicted best cloud: {best_cloud}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python train_model.py <path_to_csv>")
        sys.exit(1)

    csv_file = sys.argv[1]
    df = load_data(csv_file)

    X = df[['start_time', 'end_time', 'duration_seconds']]
    y = df['cloud']
    label_map = dict(enumerate(df['cloud'].astype('category').cat.categories))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    best_model = train_and_select_best(X_train, y_train, X_test, y_test)

    # Predict using best model on mean duration (simulated test point)
    avg_features = pd.DataFrame([X.mean()])
    predicted_index = best_model.predict(avg_features)[0]

    save_outputs(best_model, predicted_index, label_map)

if __name__ == '__main__':
    main()
