
def _assertion_supported() -> bool:
    try:
        assert False
    except AssertionError:
        return True
    else:
        return False  # type: ignore[unreachable]

