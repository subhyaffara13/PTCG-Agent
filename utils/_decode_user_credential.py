
def _decode_user_credential(stored: str) -> Optional[str]:
    """Read back a value persisted in ``LiteLLM_MCPUserCredentials.credential_b64``.

    Tries nacl decryption first (current write format).  Falls back to a
    plain ``urlsafe_b64decode`` for rows persisted by older code that wrote
    the credential without encryption.  Returns ``None`` when neither path
    yields a valid string.
    """
    decrypted = decrypt_value_helper(
        value=stored,
        key="mcp_user_credential",
        exception_type="debug",
        return_original_value=False,
    )
    if decrypted is not None:
        return decrypted
    try:
        return base64.urlsafe_b64decode(stored).decode()
    except (binascii.Error, UnicodeDecodeError, ValueError, TypeError):
        return None

