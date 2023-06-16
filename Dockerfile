FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc


RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#Какие то измнеения