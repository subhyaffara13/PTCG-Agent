from typing import Optional

def _safe_read_response(
    response: httpx.Response, timeout: Optional[float] = None
) -> bytes:
    """Safely read sync response body, falling back to empty bytes on errors."""
    try:
        if timeout is not None:
            future = _STREAMING_ERROR_BODY_READ_EXECUTOR.submit(response.read)
            try:
                return future.result(timeout=timeout)
            except Exception:
                response.close()
                return b""
        return response.read()
    except Exception:
        return b""

