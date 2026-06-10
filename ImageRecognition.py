import os
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# === CONFIG ===
input_csv = "ClassifiedBursts/Image_Labels.csv"
output_model_path = "MachineLearning/rf_model.pkl"
label_column = "99%_Verify"

# === LOAD DATA ===
df = pd.read_csv(input_csv)

# Drop rows where label is missing or NaN
df = df[pd.notna(df[label_column])]

# Separate features and labels
labels = df[label_column].to_numpy()
features = df.drop(columns=[
    'Prop_Verify', '95%_Verify', '99%_Verify', 'Burst_PNG', 'Burst_Name'
]).values  # These are the image pixels

# === TRAIN / TEST SPLIT ===
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, stratify=labels, random_state=42
)

# === TRAIN MODEL ===
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# === EVALUATE ===
train_acc = accuracy_score(y_train, clf.predict(X_train))
test_acc = accuracy_score(y_test, clf.predict(X_test))
print(f"Train Accuracy: {train_acc:.3f}")
print(f"Test Accuracy: {test_acc:.3f}")

# === SAVE MODEL ===
os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
with open(output_model_path, "wb") as f:
    pickle.dump(clf, f)

print(f"RandomForest model saved to {output_model_path}")
