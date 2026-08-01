
def _get_token_from_file_refreshed() -> str | None:
    """Get the token from `HF_TOKEN_PATH`, transparently refreshing it if close to expiry."""
    token = _get_token_from_file()
    if token is None:
        return None
    return _refresh_oauth_token_if_needed(token)

