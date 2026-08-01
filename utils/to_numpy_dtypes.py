
def to_numpy_dtypes(dtypes):
    """convert list of string dtypes to numpy dtype"""
    return [getattr(np, dt) for dt in dtypes if isinstance(dt, str)]

