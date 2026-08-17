import redis

from app.core.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_PASSWORD,
)


class RedisService:
    """
    Handles Redis connection and basic operations.
    """

    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD or None,
            decode_responses=True,
        )

    def ping(self) -> bool:
        """
        Check whether Redis is available.
        """
        return self.client.ping()

    def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
    ):
        """
        Store a value in Redis.
        """

        if ttl:
            return self.client.setex(
                key,
                ttl,
                value,
            )

        return self.client.set(
            key,
            value,
        )

    def get(self, key: str):
        """
        Retrieve a value from Redis.
        """
        return self.client.get(key)

    def delete(self, key: str):
        """
        Delete a key from Redis.
        """
        return self.client.delete(key)


redis_service = RedisService()