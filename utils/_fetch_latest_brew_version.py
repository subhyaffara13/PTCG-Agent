
def _fetch_latest_brew_version() -> str | None:
    """Fetch the latest version of the `hf` formula from the Homebrew registry. Returns None if the request fails."""
    try:
        response = get_session().get("https://formulae.brew.sh/api/formula/hf.json", timeout=2)
        hf_raise_for_status(response)
        return response.json()["versions"]["stable"]
    except Exception:
        logger.debug("Error while fetching latest version from Homebrew.", exc_info=True)
        return None

