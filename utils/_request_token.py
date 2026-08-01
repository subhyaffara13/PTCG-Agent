
def _request_token(
    client_id: str, auth_url: str, timeout: float, cert_pair=None, client_secret=None
) -> tuple[str, datetime]:
    data = {"grant_type": "client_credentials", "client_id": client_id}
    if client_secret:
        data["client_secret"] = client_secret

    resp: Optional[httpx.Response] = None
    try:
        if cert_pair:
            with httpx.Client(cert=cert_pair) as raw_client:
                handler = HTTPHandler(client=raw_client)
                resp = handler.post(auth_url, data=data, timeout=timeout)  # type: ignore[arg-type]
                payload = resp.json()
        else:
            handler = _get_httpx_client()
            resp = handler.post(auth_url, data=data, timeout=timeout)  # type: ignore[arg-type]
            payload = resp.json()
        access_token = payload["access_token"]
        expires_in = int(payload.get("expires_in", 3600))
        expiry_date = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        return f"Bearer {access_token}", expiry_date
    except Exception as e:
        msg = resp.text if resp is not None else getattr(e, "text", str(e))
        raise RuntimeError(f"Token request failed: {msg}") from e

