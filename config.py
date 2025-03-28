import os
import rsa
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_USER = os.getenv('DB_USER')
DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_USER = os.getenv('REDIS_USER')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_DB_SESSIONS = os.getenv('REDIS_DB_SESSIONS')
REDIS_DB_BROKER = os.getenv('REDIS_DB_BROKER')
REDIS_DB_CELERY_METRICS = os.getenv('REDIS_DB_CELERY_METRICS')

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URL = f"mongo://{MONGO_USER}:{MONGO_PASSWORD}@mongodb"

ALGORITHM = os.getenv('ALGORITHM')
SECRET_AUTH_KEY = os.getenv('SECRET_AUTH_KEY')

file = open('static/secret/pub_rsa')
SECRET_PUBLIC_KEY = rsa.PublicKey.load_pkcs1(file.read().encode(), "PEM")
file.close()

file = open('static/secret/pr_rsa')
SECRET_PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(file.read().encode(), "PEM")
file.close()
