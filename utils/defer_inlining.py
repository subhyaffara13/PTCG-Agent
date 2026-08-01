
def defer_inlining() -> Generator[None, None, None]:
    global _DEFER_INLINING
    prior = _DEFER_INLINING
    try:
        _DEFER_INLINING = True
        yield
    finally:
        _DEFER_INLINING = prior

