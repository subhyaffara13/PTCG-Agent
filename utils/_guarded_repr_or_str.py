
def _guarded_repr_or_str(v):
    if isinstance(v, bytes):
        return repr(v)
    return str(v)

