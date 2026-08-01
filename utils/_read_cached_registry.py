
def _read_cached_registry(path: str, max_age: int | None) -> Registry | None:
    """Return the cached registry, or `None` if missing/stale/unreadable."""
    try:
        if not os.path.exists(path):
            return None
        if max_age is not None and (time.time() - os.path.getmtime(path)) >= max_age:
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        logger.debug("Could not read cached agent harnesses registry.", exc_info=True)
        return None

