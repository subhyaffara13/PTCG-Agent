
def get_reduction(m):
    result = getattr(m, 'reduction', None)
    if result is None:
        result = _Reduction.legacy_get_string(getattr(m, 'sizeAverage', None), True, emit_warning=False)
    if result is None:
        raise AssertionError("Expected result to not be None")
    return result

