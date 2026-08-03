import time
from typing import Dict

def _write_user_env_vars_cache(
    user_id: str, server_id: str, values: Dict[str, str]
) -> None:
    cache_key = (user_id, server_id)
    # Re-insert at the tail so eviction drops the oldest-written entry, not a
    # freshly refreshed one, and only sheds a single entry instead of wiping the
    # whole cache (which would stampede the DB).
    _user_env_vars_cache.pop(cache_key, None)
    if len(_user_env_vars_cache) >= _USER_ENV_VARS_CACHE_MAX_SIZE:
        _user_env_vars_cache.pop(next(iter(_user_env_vars_cache)), None)
    _user_env_vars_cache[cache_key] = (values, time.monotonic())

