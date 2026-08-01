
def _get_docs_url() -> Optional[str]:
    """
    Get the docs (Swagger UI) URL from the environment variables.

    - If DOCS_URL is set, return it.
    - If NO_DOCS is True, return None.
    - Otherwise, default to "/".
    """
    if docs_url := os.getenv("DOCS_URL"):
        return docs_url

    if str_to_bool(os.getenv("NO_DOCS")) is True:
        return None

    return "/"

