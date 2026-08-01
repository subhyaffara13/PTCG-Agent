
def request_device_code() -> DeviceCodeInfo:
    """Request a device code from the Hub's OAuth device authorization endpoint.

    The returned dict is normalized: `interval`, `expires_in` and `verification_uri_complete`
    are always set (server values, or sensible defaults).

    Raises:
        [`DeviceCodeError`]: If the request fails.
    """
    try:
        response = get_session().post(
            f"{constants.ENDPOINT}/oauth/device",
            data={"client_id": constants.DEVICE_CODE_OAUTH_CLIENT_ID},
            timeout=constants.HF_HUB_DOWNLOAD_TIMEOUT,
        )
        hf_raise_for_status(response)
    except httpx.HTTPError as e:
        raise DeviceCodeError(f"Failed to request device code from {constants.ENDPOINT}/oauth/device: {e}") from e
    info = response.json()
    # `interval` is optional per RFC 8628 (5s is the spec-mandated fallback); `expires_in` is
    # required but defaulted defensively so polling stays bounded if a server omits it.
    info.setdefault("interval", 5)
    info.setdefault("expires_in", 900)
    if not info.get("verification_uri_complete"):
        info["verification_uri_complete"] = info["verification_uri"]
    return cast(DeviceCodeInfo, info)

