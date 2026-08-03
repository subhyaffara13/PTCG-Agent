import time
from typing import Callable

def poll_device_token(
    device_info: DeviceCodeInfo, *, on_pending: Callable[[], None] | None = None
) -> OAuthTokenResponse:
    """Poll the token endpoint until the user authorizes the device.

    Args:
        device_info (`DeviceCodeInfo`):
            The device authorization response from [`request_device_code`].
        on_pending (`Callable`, *optional*):
            Called after each "authorization pending" response (e.g. to print a progress dot).

    Returns:
        `OAuthTokenResponse`: the full token response: `access_token`, and optionally
        `refresh_token` and `expires_in`.

    Raises:
        [`DeviceCodeError`]: If authorization is denied, the device code expires, or the server
            returns an unexpected OAuth error.
    """
    interval = device_info["interval"]
    deadline = time.monotonic() + device_info["expires_in"]
    while time.monotonic() < deadline:
        # Inconclusive responses (network blip, 5xx, gateway error page, rate limiting) must not
        # abort the login: keep polling until the device code expires (RFC 8628 section 3.5).
        # The deadline bounds the total wait even if the endpoint is genuinely broken.
        data = None
        try:
            response = get_session().post(
                f"{constants.ENDPOINT}/oauth/token",
                data={
                    "grant_type": _DEVICE_CODE_GRANT_TYPE,
                    "device_code": device_info["device_code"],
                    "client_id": constants.DEVICE_CODE_OAUTH_CLIENT_ID,
                },
                timeout=constants.HF_HUB_DOWNLOAD_TIMEOUT,
            )
            if response.status_code < 500:
                data = response.json()
        except (httpx.HTTPError, ValueError):
            pass

        if data is not None:
            if "access_token" in data:
                return cast(OAuthTokenResponse, data)

            match data.get("error"):
                case None:
                    pass  # JSON without an OAuth `error` field (proxy error page, ...): transient
                case OAuthErrorCode.AUTHORIZATION_PENDING:
                    if on_pending is not None:
                        on_pending()
                case OAuthErrorCode.SLOW_DOWN:
                    interval += 5
                case OAuthErrorCode.EXPIRED_TOKEN:
                    raise DeviceCodeError(
                        "Device code expired. Please try again.", error_code=OAuthErrorCode.EXPIRED_TOKEN
                    )
                case OAuthErrorCode.ACCESS_DENIED:
                    raise DeviceCodeError(
                        "Authorization was denied. Please try again.", error_code=OAuthErrorCode.ACCESS_DENIED
                    )
                case error:
                    raise DeviceCodeError(
                        f"OAuth error: {error} - {data.get('error_description', '')}", error_code=error
                    )

        time.sleep(interval)

    raise DeviceCodeError("Device code expired (timeout). Please try again.", error_code=OAuthErrorCode.EXPIRED_TOKEN)

