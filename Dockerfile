# Используем базовый образ Python версии 3.10 с минимальной установкой (slim)
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файл requirements.txt внутрь контейнера
COPY requirements.txt .

# Обновляем пакеты и устанавливаем компилятор gcc (необходим для некоторых пакетов Python)
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install -r requirements.txt

# Копируем все файлы проекта внутрь контейнера
COPY . .

# Открываем порт 8000, чтобы приложение могло быть доступно извне контейнера
EXPOSE 8000

# Команда, которая будет запущена при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

