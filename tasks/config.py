from celery import Celery
from config import REDIS_PASSWORD, REDIS_PORT, REDIS_USER, REDIS_HOST, SYNC_DATABASE_URL, REDIS_DB_CELERY_METRICS, \
    REDIS_DB_BROKER
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger

celery_app = Celery(
    'tasks', include=['tasks.telegram_actions'],
    broker=f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BROKER}',
    backend=f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_CELERY_METRICS}'
)

engine = create_engine(SYNC_DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)

logger.add(
    'logs/celery/log_{time:YYYY-MM-DD}.log', rotation="50 MB", compression="gz", level="INFO", diagnose=False,
    backtrace=False, colorize=True
)
