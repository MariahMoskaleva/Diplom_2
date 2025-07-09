# 🌟 Stellar Burgers API Tests

Этот репозиторий содержит автоматические тесты для REST API проекта **Stellar Burgers**.  
В качестве фреймворка используется `pytest`, а для отчётности — `Allure`.

---

## 📦 Установка

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Конфигурация

Задайте переменные окружения, например в файле `.env`:

| Переменная        | Назначение                                |
|-------------------|--------------------------------------------|
| `BASE_URL`        | Базовый URL тестируемого API              |
| `DEFAULT_HEADERS` | Заголовки по умолчанию (в JSON-формате)   |

✅ Переменные автоматически подгружаются с помощью `python-dotenv`.

Также добавьте файл-шаблон `.env.example`, чтобы другим было удобно настроиться.

---

## 🚀 Запуск тестов

Запуск всех тестов с подробным выводом:
```bash
pytest -vv
```

---

## 📊 Allure-отчёты

Для генерации и отображения отчёта Allure:
```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

---

## 🧪 Используемые технологии

- `pytest`
- `requests`
- `allure-pytest`
- `python-dotenv`

---

## 👤 Авторы

- [MariahMoskaleva](https://github.com/MariahMoskaleva)

---

## 📝 Лицензия

Свободно используйте для обучения или автоматизации тестирования.
