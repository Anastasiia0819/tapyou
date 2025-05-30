# tapyou
Проект содержит автотесты для проверки API запросов, связанных с пользователями

## Структура проекта
```bash
project/
├── config/
  ├── settings.py
├── tests/
│ ├── test_users_gender.py # Тесты для запроса списка пользователей по гендеру
│ ├── test_user_id.py # Тесты для запроса информации о пользователе по ID
├── requirements.txt # Зависимости проекта
├── pytest.ini 
└── README.md # Документация

## Стек технологий

- Python 3.10+
- `pytest` — фреймворк для запуска тестов
- `requests` — HTTP-клиент для взаимодействия с API
- `allure` — отчетность
- `pytest-html` — для генерации HTML-отчета

## Установка зависимостей
pip install -r requirements.txt

## Запуск тестов
pytest -v tests/

## Запуск 
