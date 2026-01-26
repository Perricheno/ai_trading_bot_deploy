FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копирование файлов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Обучаем модели при сборке образа
RUN python train.py

# Запуск бота
CMD ["python", "main.py"]
