
def _resolve_instance(val):
    if isinstance(val, list):
        return val[0] if len(val) > 0 else None
    return val

