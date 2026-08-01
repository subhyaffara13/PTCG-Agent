
def _unwrap_optional(x):
    if x is None:
        raise AssertionError("Unwrapping null optional")
    return x

