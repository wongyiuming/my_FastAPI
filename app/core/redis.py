import redis.asyncio as redis
from app.core.config import settings

# 初始化连接池
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)