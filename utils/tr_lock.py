
def TRLock(*args, **kwargs):
    """threading RLock"""
    try:
        from threading import RLock
        return RLock(*args, **kwargs)
    except (ImportError, OSError):  # pragma: no cover
        pass

