import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
import matplotlib.pyplot as plt
import seaborn as sns


# Функция за зареждане и предварителна обработка на данните
def load_and_preprocess_data(file_path):
    # Зареждане на CSV файла
    data = pd.read_csv(file_path)
    data = data.iloc[:, 1:]
    # Разделяне на features и target
    X = data.iloc[:, :-1]  # Всички колони освен последната
    y = data.iloc[:, -1]  # Последната колона (target)

    # Стандартизация на features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, X.columns


# Функция за оценка на модел с k-fold cross validation
def evaluate_model(model, X, y, model_name, k=10):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)

    metrics = {
        'accuracy': [],
        'precision': [],
        'recall': [],
        'f1': []
    }

    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        # Обучение на модела
        if isinstance(model, tf.keras.Model):
            model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
            y_pred = (model.predict(X_val) > 0.5).astype(int)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)

        # Изчисляване на метрики
        metrics['accuracy'].append(accuracy_score(y_val, y_pred))
        metrics['precision'].append(precision_score(y_val, y_pred))
        metrics['recall'].append(recall_score(y_val, y_pred))
        metrics['f1'].append(f1_score(y_val, y_pred))

    # Извеждане на средните стойности на метриките
    print(f"\nРезултати за {model_name}:")
    for metric, values in metrics.items():
        print(f"{metric}: {np.mean(values):.3f} (+/- {np.std(values):.3f})")

    return metrics


# Създаване на невронна мрежа
def create_neural_network(input_dim):
    model = Sequential([
        Dense(64, activation='relu', input_dim=input_dim),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model


# Визуализация на резултатите
def plot_results(all_metrics):
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    models = list(all_metrics.keys())

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(metrics))
    width = 0.25
    multiplier = 0

    for model_name, model_metrics in all_metrics.items():
        means = [np.mean(model_metrics[metric]) for metric in metrics]
        offset = width * multiplier
        rects = ax.bar(x + offset, means, width, label=model_name)
        multiplier += 1

    ax.set_ylabel('Score')
    ax.set_title('Сравнение на метрики по модели')
    ax.set_xticks(x + width, metrics)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# Основна функция
def main():
    # Зареждане и обработка на данните
    X, y, feature_names = load_and_preprocess_data('Data/shuffle_email_spam_classification.csv')

    # Създаване на моделите
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Neural Network': create_neural_network(X.shape[1])
    }

    # Оценка на всички модели
    all_metrics = {}
    for name, model in models.items():
        metrics = evaluate_model(model, X, y, name)
        all_metrics[name] = metrics

    # Визуализация на резултатите
    fig = plot_results(all_metrics)
    plt.show()

    # Feature importance за Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance.head(10), x='importance', y='feature')
    plt.title('Top 10 най-важни характеристики')
    plt.xlabel('Важност')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()