# Отчёт по домашней работе №1
## Классический жизненный цикл разработки ML-модели

## 1. Артефакты

- **GitHub:** https://github.com/1rizhik/devops_hw1
- **Docker Hub:** https://hub.docker.com/r/1rizhik/devops_hw1
- **Образ:** `1rizhik/devops_hw1:latest` (~293 MB)
- **Ветки:** `main` (release), `develop` (разработка)

## 2. Набор данных

**BankNote Authentication** (UCI ML Repository):
- 1372 образца, 4 признака: variance, skewness, curtosis, entropy
- Целевая: `class` (0 — подлинная, 1 — поддельная)
- Разделение: 80% train (1097), 20% test (275), stratify, random_state=42

## 3. Модель

- **RandomForestClassifier** (n_estimators=100, random_state=42)
- Гиперпараметры в `config/config.ini`
- Метрики на тесте:
  - **Accuracy: 0.9964**
  - **F1: 0.9959**
  - **Precision: 0.9919**
  - **Recall: 1.0000**

## 4. API-сервис

Flask-приложение (`src/app.py`):

| Эндпоинт | Метод | Описание |
|---|---|---|
| `/` | GET | HTML-форма для тестирования в браузере |
| `/health` | GET | `{"status": "ok"}` |
| `/predict` | POST | `{"features": [v, s, c, e]}` → `{"prediction": [0/1]}` |

**HTML-форма** — интерактивная проверка модели в браузере:
- Форма с 4 полями, кнопка «Проверить»
- Цветовой результат: зелёный — подлинная (0), красный — поддельная (1)

## 5. Тесты

- pytest + pytest-cov
- `tests/test_api.py` — 4 теста
- Покрытие `src/app.py`: **95%**

## 6. DVC

- `data/processed.dvc` — версионирование данных
- Remote: локальное хранилище
- Модель `models/model.pkl` — в Git (небольшая, нужна в CI)

## 7. Docker

- Базовый образ `python:3.12-slim`
- Многослойный `Dockerfile`
- `docker-compose.yml`: сервис `ml-api`, порт 5000

## 8. CI/CD (GitHub Actions)

**CI Pipeline** (`.github/workflows/ci.yml`):
- Триггеры: `pull_request` в main, `push` в main
- `test` — pytest
- `build-and-push` (только на push в main) — сборка и push образа

**CD Pipeline** (`.github/workflows/cd.yml`):
- Триггеры: `workflow_run` после CI, `workflow_dispatch`
- Pull образа, запуск контейнера, функциональные тесты по `config/scenario.json`

**Результат CD:**

[Health check] status=200
[Predict authentic banknote (class 0)] status=200
[Predict fake banknote (class 1)] status=200
All functional tests passed


## 9. Дополнительно: Jenkins Pipeline

Альтернативный CI/CD-пайплайн в Jenkins (задание: «Jenkins, Team City, Circle CI и др.»).

- Jenkins LTS в Docker-контейнере, порт 8081
- Docker-in-Docker через `/var/run/docker.sock`
- `Jenkinsfile` в корне репозитория
- Стадии: Checkout → Setup venv → Run tests → Build image → Push to DockerHub → Functional test
- **Результат:** Build #10 — SUCCESS, все стадии зелёные

## 10. Выводы

Реализован полный жизненный цикл ML-модели: данные → модель → API (+ HTML-форма) → тесты → DVC → Docker → CI → CD.

Дополнительно реализован второй CI/CD-инструмент — Jenkins.

Все требования задания выполнены.