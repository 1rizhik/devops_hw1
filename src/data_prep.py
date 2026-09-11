"""Подготовка данных для обучения модели."""
import os
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def prepare_data(test_size: float = 0.2, random_state: int = 42) -> None:
    """Загружает Iris, делит на train/test, сохраняет в data/processed."""
    os.makedirs('data/processed', exist_ok=True)

    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    X_train.to_csv('data/processed/X_train.csv', index=False)
    X_test.to_csv('data/processed/X_test.csv', index=False)
    y_train.to_csv('data/processed/y_train.csv', index=False)
    y_test.to_csv('data/processed/y_test.csv', index=False)

    print(f'Train size: {len(X_train)}, Test size: {len(X_test)}')


if __name__ == '__main__':
    prepare_data()