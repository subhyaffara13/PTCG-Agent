
def _disable_aten_to_metadata_assertions():
    global _DISABLE_ATEN_TO_ASSERTION_PASS
    orig_val = _DISABLE_ATEN_TO_ASSERTION_PASS
    _DISABLE_ATEN_TO_ASSERTION_PASS = True
    try:
        yield
    finally:
        _DISABLE_ATEN_TO_ASSERTION_PASS = orig_val

