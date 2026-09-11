"""Обучение ML-модели на датасете BankNote Authentication."""
import configparser
import json
import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def load_config(path: str = 'config/config.ini') -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(path)
    return config


def load_data():
    X_train = pd.read_csv('data/processed/X_train.csv')
    X_test = pd.read_csv('data/processed/X_test.csv')
    y_train = pd.read_csv('data/processed/y_train.csv').values.ravel()
    y_test = pd.read_csv('data/processed/y_test.csv').values.ravel()
    return X_train, X_test, y_train, y_test


def train_model() -> float:
    config = load_config()
    n_estimators = config.getint('model', 'n_estimators')
    random_state = config.getint('model', 'random_state')

    X_train, X_test, y_train, y_test = load_data()

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary')

    print(f'Accuracy:  {accuracy:.4f}')
    print(f'F1:        {f1:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall:    {recall:.4f}')

    os.makedirs('models', exist_ok=True)
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('metrics.json', 'w') as f:
        json.dump(
            {
                'accuracy': accuracy,
                'f1': f1,
                'precision': precision,
                'recall': recall,
            },
            f,
            indent=2,
        )

    return accuracy


if __name__ == '__main__':
    train_model()