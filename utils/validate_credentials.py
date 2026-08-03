from typing import Optional

def validate_credentials(
    auth_url: Optional[str] = None,
    base_url: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    cert_str: Optional[str] = None,
    key_str: Optional[str] = None,
    cert_file_path: Optional[str] = None,
    key_file_path: Optional[str] = None,
) -> None:
    """
    Validate SAP AI Core credentials for completeness and consistency.

    Args:
        auth_url: OAuth2 token endpoint URL (required)
        base_url: SAP AI Core API base URL (required)
        client_id: OAuth2 client ID (required)
        client_secret: OAuth2 client secret (for secret-based auth)
        cert_str: PEM-encoded certificate string (for cert-based auth)
        key_str: PEM-encoded private key string (for cert-based auth)
        cert_file_path: Path to certificate file (for file-based cert auth)
        key_file_path: Path to private key file (for file-based cert auth)

    Raises:
        ValueError: If required fields are missing or authentication mode is ambiguous.

    Note:
        - This function does NOT validate resource_group (resolved separately).
        - Exactly one authentication method must be provided:
          * client_secret, OR
          * (cert_str AND key_str), OR
          * (cert_file_path AND key_file_path)
    """
    if not auth_url or not client_id or not base_url:
        raise ValueError(
            "SAP AI Core credentials not found. "
            "Please provide credentials by setting appropriate environment variables "
            "(e.g. AICORE_CLIENT_ID, AICORE_CLIENT_SECRET, etc.)"
        )

    modes = [
        bool(client_secret),
        bool(cert_str) and bool(key_str),
        bool(cert_file_path) and bool(key_file_path),
    ]
    if sum(bool(m) for m in modes) != 1:
        raise ValueError(
            "SAP AI Core credentials are incomplete. "
            "Invalid credentials: provide exactly one of client_secret, "
            "(cert_str & key_str), or (cert_file_path & key_file_path)."
        )

