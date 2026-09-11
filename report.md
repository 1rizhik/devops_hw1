# Отчёт по домашней работе: ML CI/CD Pipeline

## 1. Репозиторий и артефакты

- **GitHub:** https://github.com/1rizhik/devops_hw1
- **Docker Hub:** https://hub.docker.com/r/1rizhik/devops_hw1
- **Ветки:** `main` (release), `develop` (разработка)
- **Образ:** `1rizhik/devops_hw1:latest`

## 2. Набор данных

Iris (встроен в scikit-learn): 150 образцов, 3 класса, 4 признака.
Разделение: 80% train (120), 20% test (30), stratify, random_state=42.

## 3. Модель

- Алгоритм: **RandomForestClassifier** (n_estimators=100, random_state=42)
- Гиперпараметры в `config/config.ini`
- Метрики на тесте:
  - **Accuracy: 0.9000**
  - **F1 weighted: 0.8997**

## 4. API

Flask-сервис (`src/app.py`):
- `GET /health` → `{"status": "ok"}`
- `POST /predict` с `{"features": [f1, f2, f3, f4]}` → `{"prediction": [class_id]}`

## 5. Тесты

- Фреймворк: pytest + pytest-cov
- Покрытие `src/app.py`: **95%**
- Файл: `tests/test_api.py` (4 теста)

## 6. DVC

- Данные: `data/processed.dvc` (4 CSV)
- Модель: `models/model.pkl.dvc`
- Remote: локальное хранилище `C:\Learning\dvc-storage`

## 7. Docker

- Базовый образ: `python:3.12-slim`
- Dockerfile: многослойный, зависимости отдельным слоем
- docker-compose: сервис `ml-api`, порт 5000

## 8. CI Pipeline (GitHub Actions)

Файл: `.github/workflows/ci.yml`

Триггеры:
- `pull_request` в `main` → job `test`
- `push` в `main` → job `test` + `build-and-push`

Jobs:
1. **test** — установка Python 3.12, зависимостей, запуск `pytest --cov`
2. **build-and-push** (только на push в main) — сборка Docker-образа, push тегов `latest` и `<sha>` в Docker Hub

Скриншот CI #3 (Success): все jobs зелёные, длительность 2m 34s.

## 9. CD Pipeline (GitHub Actions)

Файл: `.github/workflows/cd.yml`

Триггеры:
- `workflow_run` после успешного CI Pipeline на main
- `workflow_dispatch` (вручную)

Job `functional-test`:
1. Pull образа из Docker Hub
2. Запуск контейнера на порту 5000
3. Функциональные тесты по `config/scenario.json`
4. Логи + остановка контейнера

Результат:
[Health check] status=200
[Predict setosa] status=200
[Predict virginica] status=200
All functional tests passed


## 10. Ссылки на скриншоты

- CI Pipeline (Success): скриншот 1
- CD Pipeline (Success): скриншот 2
- Docker Hub (образ): скриншот 3
- История коммитов: скриншот 4

## 11. Выводы

Реализован полный жизненный цикл ML-модели:
подготовка данных → обучение → API → тесты → DVC → Docker → CI/CD.
Автоматическая сборка образа запускается на push в main после merge PR,
функциональное тестирование контейнера — автоматически после CI.