import json
from typing import Any

def json_response(
    data: Any = sentinel,
    *,
    text: str | None = None,
    body: bytes | None = None,
    status: int = 200,
    reason: str | None = None,
    headers: LooseHeaders | None = None,
    content_type: str = "application/json",
    dumps: JSONEncoder = json.dumps,
) -> Response:
    if data is not sentinel:
        if text or body:
            raise ValueError("only one of data, text, or body should be specified")
        else:
            text = dumps(data)
    return Response(
        text=text,
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
    )

