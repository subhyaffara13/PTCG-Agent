from typing import Any

def _forward_from_src(src: str, globals: dict[str, Any], co_fields=None):
    return _method_from_src(
        method_name="forward", src=src, globals=globals, co_fields=co_fields
    )

