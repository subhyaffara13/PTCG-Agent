from typing import Any

def json_bytes_response(
    data: Any = sentinel,
    *,
    dumps: JSONBytesEncoder,
    body: bytes | None = None,
    status: int = 200,
    reason: str | None = None,
    headers: LooseHeaders | None = None,
    content_type: str = "application/json",
) -> Response:
    """Create a JSON response using a bytes-returning encoder.

    Use this when your JSON encoder (like orjson) returns bytes
    instead of str, avoiding the encode/decode overhead.
    """
    if data is not sentinel:
        if body is not None:
            raise ValueError("only one of data or body should be specified")
        else:
            body = dumps(data)
    return Response(
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
    )

