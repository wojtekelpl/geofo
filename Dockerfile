# Dla Google Cloud Run
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
CMD exec gunicorn -b :$PORT -w 2 --timeout 120 app:app
