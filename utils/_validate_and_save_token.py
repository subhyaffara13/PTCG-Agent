
def _validate_and_save_token(
    token: str,
    add_to_git_credential: bool,
    refresh_token: str | None = None,
    expires_at: int | None = None,
) -> tuple[str, str]:
    """Validate a token against the Hub, save it to the stored tokens file and set it as active.

    The token is stored under its `displayName` from the whoami response, or `oauth-{username}`
    for OAuth tokens (which have no display name).

    Args:
        token (`str`):
            The access token.
        add_to_git_credential (`bool`):
            Whether to save the token to the git credential helpers.
        refresh_token (`str`, *optional*):
            OAuth refresh token to persist alongside the access token.
        expires_at (`int`, *optional*):
            Unix timestamp at which the access token expires.

    Returns:
        `tuple[str, str]`: The token name and the username.
    """
    from .hf_api import whoami  # avoid circular import

    if token.startswith("api_org"):
        raise ValueError("You must use your personal account token, not an organization token.")

    token_info = whoami(token)
    username = token_info["name"]

    access_token_info = (token_info.get("auth") or {}).get("accessToken") or {}
    if role := access_token_info.get("role"):
        logger.info(f"Token is valid (permission: {role}).")
    else:
        logger.info("Token is valid.")

    token_name = access_token_info.get("displayName") or f"oauth-{username}"

    # Store token locally
    _save_token(token=token, token_name=token_name, refresh_token=refresh_token, expires_at=expires_at)
    # Set active token
    _set_active_token(token_name=token_name, add_to_git_credential=add_to_git_credential)
    logger.info("Login successful.")
    if _get_token_from_environment():
        logger.warning(
            "Note: Environment variable`HF_TOKEN` is set and is the current active token independently from the token you've just configured."
        )
    else:
        logger.info(f"The current active token is: `{token_name}`")
    return token_name, username

