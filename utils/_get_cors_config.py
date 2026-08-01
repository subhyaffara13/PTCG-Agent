
def _get_cors_config(
    cors_origins_env: Optional[str] = None,
    cors_credentials_env: Optional[str] = None,
):
    """
    Compute CORS allowed origins and credentials flag from environment variables.

    Extracted into a function so it can be unit-tested without reloading the module.

    Args:
        cors_origins_env: Value of LITELLM_CORS_ORIGINS (defaults to os.getenv).
        cors_credentials_env: Value of LITELLM_CORS_ALLOW_CREDENTIALS (defaults to os.getenv).

    Returns:
        Tuple[List[str], bool]: (origins, allow_credentials)
    """
    _origins_raw = (
        cors_origins_env
        if cors_origins_env is not None
        else os.getenv("LITELLM_CORS_ORIGINS")
    )
    if _origins_raw is None or _origins_raw.strip() == "":
        computed_origins = ["*"]
    else:
        computed_origins = [o.strip() for o in _origins_raw.split(",") if o.strip()]

    # Disable credentials by default when wildcard origins are used — combining
    # allow_origins=["*"] with allow_credentials=True causes Starlette to reflect
    # the incoming Origin header, allowing any site to make credentialed requests.
    # Set LITELLM_CORS_ALLOW_CREDENTIALS=true to explicitly restore the old behaviour
    # (e.g. for non-browser clients that relied on the Access-Control-Allow-Credentials
    # header being present regardless of origin).
    _credentials_raw = (
        cors_credentials_env
        if cors_credentials_env is not None
        else os.getenv("LITELLM_CORS_ALLOW_CREDENTIALS")
    )
    if _credentials_raw is not None:
        computed_credentials = _credentials_raw.strip().lower() == "true"
    else:
        computed_credentials = "*" not in computed_origins

    return computed_origins, computed_credentials

