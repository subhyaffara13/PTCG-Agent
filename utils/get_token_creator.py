
def get_token_creator(
    service_key: Optional[Union[str, dict]] = None,
    profile: Optional[str] = None,
    *,
    timeout: float = 30.0,
    expiry_buffer_minutes: int = 60,
    **overrides,
) -> Tuple[Callable[[], str], str, str]:
    """
    Creates a callable that fetches and caches an OAuth2 bearer token
    using credentials from `fetch_credentials()`.

    The callable:
      - Automatically loads credentials via fetch_credentials(profile, **overrides)
      - Fetches a new token only if expired or near expiry
      - Caches token thread-safely with a configurable refresh buffer

    Args:
        profile: Optional AICore profile name
        timeout: Timeout for HTTP requests
        expiry_buffer_minutes: Refresh the token this many minutes before expiry
        overrides: Any explicit credential overrides (client_id, client_secret, etc.)

    Returns:
        Callable[[], str]: function returning a valid "Bearer <token>" string.
    """

    # Resolve credentials using your helper
    credentials: Dict[str, str] = fetch_credentials(
        service_key=service_key, profile=profile, **overrides
    )

    auth_url = credentials.get("auth_url")
    base_url = credentials.get("base_url")
    client_id = credentials.get("client_id")
    client_secret = credentials.get("client_secret")
    cert_str = credentials.get("cert_str")
    key_str = credentials.get("key_str")
    cert_file_path = credentials.get("cert_file_path")
    key_file_path = credentials.get("key_file_path")

    # Sanity check
    validate_credentials(
        auth_url,
        base_url,
        client_id,
        client_secret,
        cert_str,
        key_str,
        cert_file_path,
        key_file_path,
    )

    lock = Lock()
    token: Optional[str] = None
    token_expiry: Optional[datetime] = None

    def _fetch_token() -> tuple[str, datetime]:
        # Case 1: secret-based auth
        if client_secret:
            return _request_token(
                auth_url=auth_url,  # type: ignore[arg-type]
                client_id=client_id,  # type: ignore[arg-type]
                timeout=timeout,
                client_secret=client_secret,
            )
        # Case 2: cert/key strings
        if cert_str and key_str:
            cert_str_fixed = cert_str.replace("\\n", "\n")
            key_str_fixed = key_str.replace("\\n", "\n")
            with tempfile.TemporaryDirectory() as tmp:
                cert_path = os.path.join(tmp, "cert.pem")
                key_path = os.path.join(tmp, "key.pem")
                with open(cert_path, "w") as f:
                    f.write(cert_str_fixed)
                with open(key_path, "w") as f:
                    f.write(key_str_fixed)
                return _request_token(
                    auth_url=auth_url,  # type: ignore[arg-type]
                    client_id=client_id,  # type: ignore[arg-type]
                    timeout=timeout,
                    cert_pair=(cert_path, key_path),
                )
        # Case 3: file-based cert/key
        if cert_file_path is not None and key_file_path is not None:
            return _request_token(
                auth_url=auth_url,  # type: ignore[arg-type]
                client_id=client_id,  # type: ignore[arg-type]
                timeout=timeout,
                cert_pair=(cert_file_path, key_file_path),
            )
        # Defensive guard: should never reach here due to validate_credentials()
        raise ValueError(
            "Invalid authentication configuration: no valid credentials found. "
        )

    def get_token() -> str:
        nonlocal token, token_expiry
        with lock:
            now = datetime.now(timezone.utc)
            if (
                token is None
                or token_expiry is None
                or token_expiry - now < timedelta(minutes=expiry_buffer_minutes)
            ):
                token, token_expiry = _fetch_token()
            return token

    return get_token, credentials["base_url"], credentials["resource_group"]

