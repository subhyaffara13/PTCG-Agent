
def _get_openapi_url() -> Optional[str]:
    """
    Get the OpenAPI JSON URL from the environment variables.

    - If OPENAPI_URL is set, return it.
    - If NO_OPENAPI is True, return None.
    - Otherwise, default to "/openapi.json".
    """
    if openapi_url := os.getenv("OPENAPI_URL"):
        return openapi_url

    if str_to_bool(os.getenv("NO_OPENAPI")) is True:
        return None

    return "/openapi.json"

