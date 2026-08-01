
def disable_info_traces() -> Iterator[None]:
    """
    Temporarily disable info traces.
    """
    from distutils import log

    saved = log.set_threshold(log.WARN)
    try:
        yield
    finally:
        log.set_threshold(saved)

