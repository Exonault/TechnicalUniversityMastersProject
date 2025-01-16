import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical


# Load dataset
def load_and_preprocess_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    data = data.iloc[:, 1:]

    # Separate features (X) and target (y)
    X = data.iloc[:, :-1]  # All columns except the last
    y = data.iloc[:, -1]  # The last column (spam or not spam)

    # Standardize features (optional but recommended for some models)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


# Evaluate model using cross-validation
def evaluate_model(model, X, y, cv=5):
    kfold = KFold(n_splits=cv, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=kfold, scoring='accuracy')
    return scores


# Visualize performance comparison
def plot_model_performance(models, scores):
    fig, ax = plt.subplots(figsize=(10, 6))

    for model_name, model_scores in scores.items():
        ax.plot(range(1, len(model_scores) + 1), model_scores, marker='o', label=model_name)

    ax.set_title("Model Performance Across Folds")
    ax.set_xlabel("Fold")
    ax.set_ylabel("Accuracy")
    ax.legend()
    plt.show()


# Main workflow
file_path = "Data/shuffle_email_spam_classification.csv"  # Adjust the file path as needed
X, y = load_and_preprocess_data(file_path)

# Split the data for initial evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression
logistic_model = LogisticRegression(random_state=42)
logistic_model.fit(X_train, y_train)
y_pred_logistic = logistic_model.predict(X_test)

# Decision Tree
tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train, y_train)
y_pred_tree = tree_model.predict(X_test)

# Evaluate models
logistic_scores = evaluate_model(logistic_model, X, y, cv=5)
tree_scores = evaluate_model(tree_model, X, y, cv=5)

# Compile results
model_scores = {
    "Logistic Regression": logistic_scores,
    "Decision Tree": tree_scores
}

plot_model_performance(model_scores, model_scores)

# Display metrics
print("Logistic Regression Metrics:")
print(classification_report(y_test, y_pred_logistic))
print("Decision Tree Metrics:")
print(classification_report(y_test, y_pred_tree))

# Bonus: Neural Network
nn_model = Sequential([
    Dense(32, activation='relu', input_shape=(X.shape[1],)),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

nn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = nn_model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2, verbose=1)

# Evaluate Neural Network
nn_loss, nn_accuracy = nn_model.evaluate(X_test, y_test, verbose=0)
print(f"Neural Network Accuracy: {nn_accuracy:.2f}")

# Plot Neural Network training history
plt.figure(figsize=(10, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Neural Network Accuracy Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Compare final results
print("Model Comparison:")
print(f"Logistic Regression: {np.mean(logistic_scores):.2f} (+/- {np.std(logistic_scores):.2f})")
print(f"Decision Tree: {np.mean(tree_scores):.2f} (+/- {np.std(tree_scores):.2f})")
print(f"Neural Network: {nn_accuracy:.2f}")
