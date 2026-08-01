
def get_token_to_send(token: bool | str | None) -> str | None:
    """Select the token to send from either `token` or the cache."""
    # Case token is explicitly provided
    if isinstance(token, str):
        return token

    # Case token is explicitly forbidden
    if token is False:
        return None

    # Case token is explicitly required
    if token is True:
        cached_token = get_token()
        if cached_token is None:
            raise LocalTokenNotFoundError(
                "Token is required (`token=True`), but no token found. You"
                " need to provide a token or be logged in to Hugging Face with"
                " `hf auth login` or `huggingface_hub.login`. See"
                " https://huggingface.co/settings/tokens."
            )
        return cached_token

    # Case implicit use of the token is forbidden by env variable. Checked before resolving the
    # cached token: `get_token()` may refresh an OAuth token (network call + file writes), which
    # must not happen when the resolved token wouldn't be used anyway.
    if constants.HF_HUB_DISABLE_IMPLICIT_TOKEN:
        return None

    # Otherwise: we use the cached token as the user has not explicitly forbidden it
    return get_token()

