# devops_hw1 — ML CI/CD Pipeline

Домашняя работа: классический жизненный цикл разработки ML-модели.
# devops_hw1 — ML CI/CD Pipeline

## Описание
End-to-end MLOps пайплайн для модели классификации Iris.

## Стек
- Python 3.14 / scikit-learn / Flask
- DVC для версионирования данных и модели
- Docker + Docker Hub
- GitHub Actions (CI/CD)

## Компоненты
- `src/data_prep.py` — подготовка данных
- `src/train.py` — обучение RandomForest (accuracy 0.9)
- `src/app.py` — Flask API
- `tests/test_api.py` — pytest (coverage 95%)
- `.github/workflows/` — CI/CD pipelines

## Ссылки
- Docker Hub: https://hub.docker.com/r/1rizhik/devops_hw1
- CI/CD: GitHub Actions

## Запуск
```bash
pip install -r requirements.txt
python src/data_prep.py
python src/train.py
python src/app.py