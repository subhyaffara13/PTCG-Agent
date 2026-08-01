
def _fetch_latest_pypi_version(library: str) -> str | None:
    """Fetch the latest version of a library from PyPI. Returns None if the request fails."""
    try:
        response = get_session().get(f"https://pypi.org/pypi/{library}/json", timeout=2)
        hf_raise_for_status(response)
        return response.json()["info"]["version"]
    except Exception:
        logger.debug("Error while fetching latest version from PyPI.", exc_info=True)
        return None

