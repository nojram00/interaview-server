FROM python:3.13.1-slim

WORKDIR /app

COPY . /app/
COPY .env /app/.env

RUN pip install -r requirements.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]