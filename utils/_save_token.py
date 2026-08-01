
def _save_token(
    token: str, token_name: str, *, refresh_token: str | None = None, expires_at: int | None = None
) -> None:
    """
    Save the given token.

    If the stored tokens file does not exist, it will be created.
    Args:
        token (`str`):
            The token to save.
        token_name (`str`):
            The name of the token.
        refresh_token (`str`, *optional*):
            OAuth refresh token used to renew the access token when it expires.
        expires_at (`int`, *optional*):
            Unix timestamp at which the access token expires.
    """
    stored_tokens = _read_stored_tokens_full()
    fields = {"hf_token": token}
    if refresh_token is not None:
        fields["refresh_token"] = refresh_token
    if expires_at is not None:
        fields["expires_at"] = str(expires_at)
    # Replace the whole section: re-logging in under the same name must drop stale metadata.
    stored_tokens[token_name] = fields
    _save_stored_tokens_full(stored_tokens)
    logger.info(f"The token `{token_name}` has been saved to {constants.HF_STORED_TOKENS_PATH}")

