# Structured Extraction Service (Support Tickets)

Цей проєкт є першою частиною наскрізного проєкту курсу AI Engineering. Сервіс призначений для витягування структурованих даних із сирих (і частково «брудних») текстів тікетів техпідтримки за допомогою LLM (наразі використовується `gemini-3.5-flash-lite`) та їх валідації через Pydantic.

## 📂 Структура проєкту

```text
r_d_lesson_1/
├── data/
│   ├── tickets.json          # 30 сирих текстів тікетів (різні мови, помилки, відсутні поля)
│   └── golden_set.json       # 10 еталонних розмічених JSON для замірів точності
├── prompts/
│   └── v1_baseline.txt       # Базовий промпт для витягування даних
├── results/                  # Згенеровані LLM файли зберігаються тут
├── src/
│   ├── extractor.py          # Логіка роботи з Gemini API (retry, timeout)
│   └── schema.py             # Pydantic-схема вихідних даних
├── .env.example              # Шаблон змінних середовища
├── main.py                   # Точка входу для запуску пайплайну
└── requirements.txt          # Залежності Python
```

## 🛠 Вимоги

*   **Python:** 3.11 або вище.
*   API-ключ від **Google AI Studio** (Gemini).

## 🚀 Встановлення та налаштування

1. **Клонуйте репозиторій та перейдіть у папку проєкту:**
   ```bash
   git clone <ваше-посилання-на-репо>
   cd r_d_lesson_1
   ```

2. **Створіть та активуйте віртуальне середовище:**
   ```bash
   # Для Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Для macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Налаштуйте змінні середовища:**
   Створіть файл `.env` у корені проєкту (скопіювавши шаблон з `.env.example`) та додайте ваш API-ключ:
   ```bash
   cp .env.example .env
   ```
   Відкрийте `.env` і вставте ваш ключ:
   ```env
   GEMINI_API_KEY=ваш_реальний_ключ_тут
   ```

## ▶️ Запуск

Проєкт запускається однією командою. Скрипт автоматично підхопить промпт, прожене всі тікети з `data/tickets.json` через модель та збереже результат у папку `results/`.

```bash
python main.py
```

Після успішного завершення у терміналі з'явиться повідомлення про збереження файлу (наприклад, `results/v1_baseline_gemini-3.5-flash-lite.json`).