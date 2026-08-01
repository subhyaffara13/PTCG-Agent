
def enter_freezing() -> Generator[Any, None, None]:
    """
    Context manager to designate when freezing is active.
    """
    prev = _freezing_active()
    _TLS.freezing_active = True
    try:
        yield
    finally:
        _TLS.freezing_active = prev

