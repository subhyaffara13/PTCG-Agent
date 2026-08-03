from typing import Optional

def _get_client_cache_key(
    model: str, vertex_project: Optional[str], vertex_location: Optional[str]
):
    _cache_key = f"{model}-{vertex_project}-{vertex_location}"
    return _cache_key

