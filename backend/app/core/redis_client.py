import os
import redis.asyncio as redis
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "redis-service")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.password = os.getenv("REDIS_PASSWORD", None)
        self.client = None

    async def connect(self):
        logger.info(f"Connecting to Redis at {self.host}:{self.port}")
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=True
            )
            await self.client.ping()
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise e

    async def close(self):
        if self.client:
            await self.client.close()

redis_client = RedisClient()
