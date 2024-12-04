FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

COPY requirements.txt .

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]

EXPOSE 8000
