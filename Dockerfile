FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY simple_twitter_discord_bot/main.py .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]

