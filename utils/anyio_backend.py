from typing import Any

def anyio_backend(request: Any) -> Any:
    return request.param

