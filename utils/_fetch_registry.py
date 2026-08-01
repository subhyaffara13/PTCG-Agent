
def _fetch_registry() -> Registry | None:
    """Fetch the registry from the Hub. Returns `None` when offline or on any error."""
    if constants.HF_HUB_OFFLINE:
        return None
    try:
        from ._http import get_session

        response = get_session().get(
            f"{constants.ENDPOINT}/api/agent-harnesses",
            timeout=_REGISTRY_FETCH_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        logger.debug("Could not fetch agent harnesses registry from the Hub.", exc_info=True)
        return None

