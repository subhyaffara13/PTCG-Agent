import time

def _save_oauth_token(response: OAuthTokenResponse) -> tuple[str, str]:
    """Validate and persist a token response from the device code flow, including refresh metadata."""
    expires_in = response.get("expires_in")
    token_name, username = _validate_and_save_token(
        response["access_token"],
        add_to_git_credential=False,
        refresh_token=response.get("refresh_token"),
        expires_at=int(time.time()) + int(expires_in) if expires_in else None,
    )
    if note := _expiration_note(response):
        logger.info(f"Note: {note}")
    return token_name, username

