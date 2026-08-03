from typing import Any

def _lazy_import_caching(name: str) -> Any:
    """Handler for caching classes (Cache, DualCache, RedisCache, etc.)"""
    return _generic_lazy_import(name, _CACHING_IMPORT_MAP, "Caching")

