
def _warn_refresh_failure_once(message: str) -> None:
    global _OAUTH_REFRESH_WARNED
    if not _OAUTH_REFRESH_WARNED:
        logger.warning(message)
        _OAUTH_REFRESH_WARNED = True

