from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from contextlib import asynccontextmanager

from api.src import router
from api.src.models.db_client import create_tables
from api.src.redis.redis_client import init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await init_redis()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=router)

if __name__ == '__main__':
    try:
        run(app, port=8080, ssl_keyfile='./certs/key.pem', ssl_certfile='./certs/cert.pem')
    except Exception as e:
        print('exit', e)
