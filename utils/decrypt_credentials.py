
def decrypt_credentials(
    credentials: MCPCredentials,
) -> MCPCredentials:
    """Decrypt all secret fields in an MCPCredentials dict using the global salt key."""
    secret_fields = [
        "auth_value",
        "client_id",
        "client_secret",
        "aws_access_key_id",
        "aws_secret_access_key",
        "aws_session_token",
    ]
    for field in secret_fields:
        value = credentials.get(field)  # type: ignore[literal-required]
        if value is not None and isinstance(value, str):
            credentials[field] = decrypt_value_helper(  # type: ignore[literal-required]
                value=value,
                key=field,
                exception_type="debug",
                return_original_value=True,
            )
    return credentials

