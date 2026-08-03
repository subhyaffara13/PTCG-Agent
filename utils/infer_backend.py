from typing import Any

def infer_backend(x: Any) -> str:
    return _infer_backend_class_cached(x.__class__)

