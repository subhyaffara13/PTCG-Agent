from typing import Tuple

def _parse_token_response(response: httpx.Response) -> Tuple[str, int]:
    """Parse OAuth token response."""
    data = response.json()

    # GigaChat returns either 'tok'/'exp' or 'access_token'/'expires_at'
    access_token = data.get("tok") or data.get("access_token")
    expires_at = data.get("exp") or data.get("expires_at")

    if not access_token:
        raise GigaChatAuthError(
            status_code=500,
            message=f"Invalid token response: {data}",
        )

    # expires_at is in milliseconds
    if isinstance(expires_at, str):
        expires_at = int(expires_at)

    verbose_logger.debug("GigaChat access token obtained successfully")
    return access_token, expires_at


def _parse_token_response(response: httpx.Response) -> dict:
    try:
        return response.json()
    except ValueError as e:
        raise DeviceCodeError(
            f"Failed to parse response from {constants.ENDPOINT}/oauth/token "
            f"(status {response.status_code}): {response.text[:500]}"
        ) from e

