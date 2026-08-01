
def _is_supported_upgrade(headers: CIMultiDictProxy[str]) -> bool:
    """Check if the upgrade header is supported."""
    u = headers.get(hdrs.UPGRADE, "")
    # .lower() can transform non-ascii characters.
    return u.isascii() and u.lower() in {"tcp", "websocket"}

