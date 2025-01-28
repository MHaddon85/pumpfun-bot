# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "main.py"]

# requirements.txt
python-telegram-bot==20.3
requests==2.31.0
sqlalchemy==2.0.23
pandas==2.1.1