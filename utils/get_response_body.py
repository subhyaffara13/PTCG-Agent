from typing import Optional

def get_response_body(response: httpx.Response) -> Optional[dict]:
    try:
        return response.json()
    except Exception:
        return None

