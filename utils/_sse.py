import json

def _sse(event: SSEEvent) -> str:
    return f"data: {json.dumps(event)}\n\n"

