import uuid
from typing import Tuple

def _request_token_sync(
    credentials: str,
    scope: str,
    auth_url: str,
) -> Tuple[str, int]:
    """
    Request new access token from GigaChat OAuth endpoint (sync).

    Returns:
        Tuple of (access_token, expires_at_ms)
    """
    headers = {
        "Authorization": f"Basic {credentials}",
        "RqUID": str(uuid.uuid4()),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"scope": scope}

    verbose_logger.debug(f"Requesting GigaChat access token from {auth_url}")

    try:
        client = _get_http_client()
        response = client.post(auth_url, headers=headers, data=data, timeout=30)
        response.raise_for_status()
        return _parse_token_response(response)
    except httpx.HTTPStatusError as e:
        raise GigaChatAuthError(
            status_code=e.response.status_code,
            message=f"GigaChat authentication failed: {e.response.text}",
        )
    except httpx.RequestError as e:
        raise GigaChatAuthError(
            status_code=500,
            message=f"GigaChat authentication request failed: {str(e)}",
        )

