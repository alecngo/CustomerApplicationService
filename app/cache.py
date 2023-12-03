import redis
import os

class RedisSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_redis()
        return cls._instance

    def _init_redis(self):
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")
        redis_password = os.getenv("REDIS_PASSWORD")

        if all([redis_host, redis_port, redis_password]):
            self.client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                decode_responses=True  # Automatically decode responses to Python strings
            )
        else:
            raise EnvironmentError("REDIS_HOST, REDIS_PORT, and REDIS_PASSWORD environment variables must be set.")

# Usage
redis_instance = RedisSingleton()
redis_client = redis_instance.client