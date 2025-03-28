FROM python:3.11

WORKDIR app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#COPY ../.. /app

CMD ["celery", "-A", "app.tasks.config.celery_app worker"]
