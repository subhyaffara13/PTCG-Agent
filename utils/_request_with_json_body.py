import json
from typing import List

def _request_with_json_body(body: dict) -> Request:
    """Create a Starlette Request that will return the given dict as parsed JSON body."""
    body_bytes = json.dumps(body).encode()
    received: List[bool] = [False]

    async def receive() -> dict:
        if received[0]:
            return {"type": "http.disconnect"}
        received[0] = True
        return {"type": "http.request", "body": body_bytes, "more_body": False}

    scope: dict = {
        "type": "http",
        "method": "POST",
        "path": "/v1/chat/completions",
        "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
        "scheme": "http",
        "server": ("localhost", 8000),
        "client": ("127.0.0.1", 0),
        "root_path": "",
        "app": None,
        "asgi": {"version": "3.0", "spec_version": "2.0"},
    }
    return Request(scope, receive=receive)

