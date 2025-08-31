# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем зависимости для работы pip и Google API
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY bot.py /app/bot.py

# creds.json монтируется при запуске контейнера
# поэтому его копировать не нужно

# Запуск бота
CMD ["python", "bot.py"]
