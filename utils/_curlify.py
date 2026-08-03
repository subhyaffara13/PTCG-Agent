from typing import Any

def _curlify(request: httpx.Request) -> str:
    """Convert a `httpx.Request` into a curl command (str).

    Used for debug purposes only.

    Implementation vendored from https://github.com/ofw/curlify/blob/master/curlify.py.
    MIT License Copyright (c) 2016 Egor.
    """
    parts: list[tuple[Any, Any]] = [
        ("curl", None),
        ("-X", request.method),
    ]

    for k, v in sorted(request.headers.items()):
        if k.lower() == "authorization":
            v = "<TOKEN>"  # Hide authorization header, no matter its value (can be Bearer, Key, etc.)
        parts += [("-H", f"{k}: {v}")]

    body: str | None = None
    try:
        if request.content is not None:
            body = request.content.decode("utf-8", errors="ignore")
            if len(body) > 1000:
                body = f"{body[:1000]} ... [truncated]"
            body = _redact_sensitive_body(body)
    except httpx.RequestNotRead:
        body = "<streaming body>"
    if body is not None:
        parts += [("-d", body.replace("\n", ""))]

    parts += [(None, request.url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(quote(str(k)))
        if v:
            flat_parts.append(quote(str(v)))

    return " ".join(flat_parts)

