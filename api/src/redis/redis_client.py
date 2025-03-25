from redis import asyncio as aioredis


class AioRedisClient:
    def __init__(
            self,
            host: str = 'localhost',
            port: int = 6379,
            db: int = 0
    ):
        self.host = host
        self.port = port
        self.db = db
        self.redis = None

    async def create_client(self):
        if not self.redis:
            self.redis = await aioredis.Redis(host=self.host, port=self.port, db=self.db)
        return self.redis.client()

    async def close(self):
        await self.redis.close()
        await self.redis.wait_closed()



redis_client = AioRedisClient()


async def init_redis():
    if redis_client.redis:
        await redis_client.close()
    else:
        await redis_client.create_client()
