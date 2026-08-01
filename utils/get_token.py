
def get_token() -> str | None:
    """
    Get token if user is logged in.

    Note: in most cases, you should use [`huggingface_hub.utils.build_hf_headers`] instead. This method is only useful
          if you want to retrieve the token for other purposes than sending an HTTP request.

    If `HF_OIDC_RESOURCE` is set (Trusted Publishers, typically in CI), a short-lived token obtained via OIDC token
    exchange takes precedence. Otherwise the token is retrieved from the `HF_TOKEN` environment variable, then from the
    token file in the Hugging Face home folder. Returns None if user is not logged in. To log in, use [`login`] or
    `hf auth login`.

    OAuth tokens obtained with the browser-based login come with a refresh token: when such a token is close to
    expiry, it is transparently refreshed and persisted before being returned.

    Note: if `HF_OIDC_RESOURCE` is set but the OIDC token exchange fails, this raises instead of returning `None`,
    opting into OIDC is explicit, so a failure surfaces as a clear error rather than a silent fallback.

    Returns:
        `str` or `None`: The token, `None` if it doesn't exist.
    """
    return (
        _get_token_from_oidc()
        or _get_token_from_environment()
        or _get_token_from_file_refreshed()
        or _get_token_from_google_colab()
    )

