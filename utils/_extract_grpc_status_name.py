from typing import Any, Optional

def _extract_grpc_status_name(error: Any) -> Optional[str]:
    """
    Best-effort extraction of a gRPC StatusCode name from an arbitrary error.

    Works for ``grpc.RpcError`` instances (which expose ``.code()``) as well
    as plain exceptions whose string representation contains a status name.
    """
    code_fn = getattr(error, "code", None)
    if callable(code_fn):
        try:
            code = code_fn()
        except Exception:
            code = None
        name = getattr(code, "name", None)
        if isinstance(name, str):
            return name
    return None

