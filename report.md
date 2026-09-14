# Отчёт по домашней работе №1
## Классический жизненный цикл разработки ML-модели

## 1. Ссылки на артефакты

- **GitHub репозиторий:** https://github.com/1rizhik/devops_hw1
- **Docker Hub:** https://hub.docker.com/r/1rizhik/devops_hw1
- **Ветки:** `main` (release), `develop` (разработка)
- **Образ:** `1rizhik/devops_hw1:latest`

## 2. Набор данных

**BankNote Authentication** (UCI ML Repository, dataset 267):
- **1372 образца**
- **4 признака:** variance, skewness, curtosis, entropy
- **Целевая переменная:** class (0 — подлинная, 1 — поддельная)
- **Задача:** бинарная классификация
- **Разделение:** 80% train (1097), 20% test (275), stratify, random_state=42
- **Источник:** `data/raw/BankNote_Authentication.csv`

## 3. Модель

- Алгоритм: **RandomForestClassifier** (n_estimators=100, random_state=42)
- Гиперпараметры в `config/config.ini`
- Метрики на тестовой выборке:
  - **Accuracy: 0.9964**
  - **F1: 0.9959**
  - **Precision: 0.9919**
  - **Recall: 1.0000**

## 4. API-сервис

Flask-приложение (`src/app.py`):

| Эндпоинт | Метод | Описание |
|---|---|---|
| `/` | GET | HTML-форма для тестирования в браузере |
| `/health` | GET | Проверка работоспособности → `{"status": "ok"}` |
| `/predict` | POST | `{"features": [v, s, c, e]}` → `{"prediction": [0/1]}` |

### Веб-интерфейс

Помимо REST API, реализована HTML-страница для интерактивной проверки модели:
- **URL:** `http://localhost:5000/`
- **Форма:** 4 поля (variance, skewness, curtosis, entropy), кнопка «Проверить»
- **Результат:** цветовой индикатор:
  - зелёный — подлинная банкнота (класс 0)
  - красный — поддельная банкнота (класс 1)
- **Реализация:** inline HTML + JavaScript в `src/app.py`, отправляет POST на `/predict`

## 5. Тесты

- Фреймворк: pytest + pytest-cov
- Файл: `tests/test_api.py` (4 теста)
- Покрытие `src/app.py`: **95%**

## 6. DVC

- `data/processed.dvc` — версионирование подготовленных данных (4 CSV)
- Remote: `C:\Learning\dvc-storage`
- Модель `models/model.pkl` хранится в Git напрямую (файл небольшой, нужен в CI без дополнительной настройки DVC-remote)

## 7. Docker

- Базовый образ: `python:3.12-slim`
- Многослойный `Dockerfile`: зависимости отдельным слоем (кэширование)
- `docker-compose.yml`: сервис `ml-api`, порт 5000
- Docker Hub: `1rizhik/devops_hw1:latest`, размер ~293 MB

## 8. Конфигурационные файлы

- `config/config.ini` — гиперпараметры модели
- `config/scenario.json` — сценарии функционального тестирования
- `dev_sec_ops.yml` — подпись Docker-образа, метрики, хэши последних 5 коммитов
- `requirements.txt` — зависимости проекта
- `Dockerfile`, `docker-compose.yml`, `.dockerignore`

## 9. CI Pipeline (GitHub Actions)

Файл: `.github/workflows/ci.yml`

Триггеры:
- `pull_request` в `main` → job `test`
- `push` в `main` → jobs `test` + `build-and-push`

Jobs:
1. **test** — установка Python 3.12, зависимостей, запуск `pytest --cov`
2. **build-and-push** (только на push в main) — сборка Docker-образа, push тегов `latest` и `<SHA коммита>` в Docker Hub

## 10. CD Pipeline (GitHub Actions)

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
[Predict authentic banknote (class 0)] status=200
[Predict fake banknote (class 1)] status=200
All functional tests passed


## 11. Дополнительно: Jenkins Pipeline

Помимо GitHub Actions, реализован CI/CD пайплайн в **Jenkins** (задание: «Jenkins, Team City, Circle CI и др.»).

### Инфраструктура
- Jenkins LTS (JDK 17) в Docker-контейнере
- Docker-in-Docker через монтирование `/var/run/docker.sock`
- Порт Jenkins: `8081`, порт агентов: `50001`
- Credentials `dockerhub-creds` (Username with password)
- `Jenkinsfile` в корне репозитория

### Стадии Pipeline
1. **Checkout** — клонирование репозитория из GitHub (ветка main)
2. **Setup Python venv** — создание venv, установка зависимостей из `requirements.txt`
3. **Run tests** — pytest (4 теста)
4. **Build Docker image** — сборка образа с тегами `jenkins-${BUILD_NUMBER}` и `latest`
5. **Push to DockerHub** — публикация образов
6. **Functional test** — запуск контейнера, проверка `/health`, `/predict` для классов 0 и 1

### Особенности реализации
- Связь Jenkins ↔ API-контейнер через `host.docker.internal:5001` (классическая проблема Docker-in-Docker)
- Retry-цикл ожидания готовности API (до 30 секунд, шаг 1 сек)
- При падении API — автоматический вывод логов контейнера

### Результаты
- Pipeline `devops_hw1_pipeline` — **SUCCESS** (Build #10, ~57 сек)
- Все 8 стадий зелёные
- Docker-образ обновлён в Docker Hub (теги `jenkins-10`, `latest`)
- Функциональные тесты успешны:
  - `/health` → `{"status":"ok"}` (HTTP 200)
  - `/predict` (class 0) → `{"prediction":[0]}` (HTTP 200)
  - `/predict` (class 1) → `{"prediction":[1]}` (HTTP 200)

## 12. Ссылки на скриншоты

- CI Pipeline (Success): скриншот 1
- CD Pipeline (Success): скриншот 2
- Jenkins Pipeline (Success, все стадии зелёные): скриншот 3
- Jenkins Functional test — раздел `=== Run functional tests ===`: скриншот 4
- Docker Hub (образ): скриншот 5
- История коммитов: скриншот 6
- HTML-форма в браузере: скриншот 7

## 13. Выводы

Реализован полный жизненный цикл ML-модели:
подготовка данных → обучение → API (+ HTML-форма для браузера) → тесты → DVC → Docker → CI → CD.

Дополнительно реализован **второй CI/CD-инструмент — Jenkins** (8 стадий, все успешны).

Все требования задания выполнены:
- ✅ Репозиторий с историей коммитов
- ✅ Модель BankNote Authentication (accuracy 0.9964)
- ✅ Flask API + HTML-форма
- ✅ Тесты pytest (покрытие 95%)
- ✅ DVC
- ✅ Docker + Docker Hub
- ✅ CI Pipeline (GitHub Actions)
- ✅ CD Pipeline (GitHub Actions)
- ✅ Jenkins Pipeline
- ✅ Отчёт