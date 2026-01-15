import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.metrics import recall_score, f1_score, classification_report
import joblib
import os

def train_and_evaluate(X_train, X_test, y_train, y_test):
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
        "SVM": SVC(kernel="rbf", probability=True, random_state=42)
    }

    best_model = None
    best_name = ""
    best_cv_recall = 0

    for name, model in models.items():
        print(f"\n{name}:")

        # Cross-validation on training data
        cv_recall = cross_val_score(model, X_train, y_train, cv=5, scoring='recall')
        print(f"  CV Recall: {cv_recall}")
        mean_cv = cv_recall.mean()
        print(f"  Mean CV Recall: {mean_cv:.4f}")

        # Train on full training set
        model.fit(X_train, y_train)

        # Test metrics
        y_pred = model.predict(X_test)
        print(f"  Test Recall: {recall_score(y_test, y_pred):.4f}")
        print(f"  Test F1: {f1_score(y_test, y_pred):.4f}")
        print(classification_report(y_test, y_pred))

        # Select best model
        if mean_cv > best_cv_recall:
            best_cv_recall = mean_cv
            best_model = model
            best_name = name

    print(f"\nBest model: {best_name} (Mean CV Recall = {best_cv_recall:.4f})")
    return best_model, best_name

if __name__ == "__main__":
    X_train = np.load("data/X_train_processed.npy", allow_pickle=True)
    X_test = np.load("data/X_test_processed.npy", allow_pickle=True)
    y_train = np.load("data/y_train.npy", allow_pickle=True)
    y_test = np.load("data/y_test.npy", allow_pickle=True)

    best_model, best_name = train_and_evaluate(X_train, X_test, y_train, y_test)

    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model, "models/churn_model.joblib")
    print("Best model saved to models/churn_model.joblib")