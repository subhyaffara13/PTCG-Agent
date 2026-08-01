
def _get_redoc_url() -> Optional[str]:
    """
    Get the Redoc URL from the environment variables.

    - If REDOC_URL is set, return it.
    - If NO_REDOC is True, return None.
    - Otherwise, default to "/redoc".
    """
    if redoc_url := os.getenv("REDOC_URL"):
        return redoc_url

    if str_to_bool(os.getenv("NO_REDOC")) is True:
        return None

    return "/redoc"

