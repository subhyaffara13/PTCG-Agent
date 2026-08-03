from typing import Any

def _add_sharing_cache(cache: CacheType) -> Any:
    _SHARING_STACK[threading.get_ident()].append(cache)

