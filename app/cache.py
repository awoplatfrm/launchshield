import redis
from flask import current_app


class FlagCache:
    def __init__(self, port=None, host=None, db_num=0):

        self.port = port
        self.host = host
        self.db_num = db_num
        self.client = None

    @property
    def client(self):

        if self.client is None:
            port = self.port or current_app.config.get("REDIS_PORT", 6379)
            host = self.host or current_app.config.get("REDIS_HOST", " localhost")
            self.client = redis.Redis(
                host=host,
                port=port,
                db=self.db_num,
                decode_responses=True,  # return utf-8 string instead of byte
            )
        return self.client

    def _format_key(self, api_key: str, flag_key: str):

        return f"flag:{flag_key}:{api_key}"

    def get_flag(self, api_key: str, flag_key: str):

        try:
            val = self.client.get(self._format_key(api_key, flag_key))
            if val is None:
                return None
            return val.lower() == "true"
        except redis.RedisError:
            return None

    def invalidate_flag(self, api_key: str, flag_key: str):

        try:
            self.client.delete(self._format_key(api_key, flag_key))
        except redis.RedisError:
            pass


flag_cache = FlagCache()
