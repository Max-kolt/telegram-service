from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from utils import setting_database
from routers import telegram_router
from contextlib import asynccontextmanager
from database import engine, BaseModel
from loguru import logger
import uvicorn

logger.add('logger.log', rotation="500 MB", compression="gz", level="DEBUG", diagnose=False, backtrace=False)


@asynccontextmanager
async def lifespan(current_app: FastAPI):
    # Start up execution logic
    # await setting_database()
    # logger.info('Database is creating')
    yield


app = FastAPI(title="Telegram user-bots managing service", lifespan=lifespan,  root_path='/api')
app.include_router(telegram_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def welcome():
    return {"Hello": "telegram user-bots managing service"}


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

