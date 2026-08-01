
def _set_static_list_metadata(attr: str, dist: Distribution, val: list) -> None:
    """Apply distutils metadata validation but preserve "static" behaviour"""
    meta = dist.metadata
    setter, getter = getattr(meta, f"set_{attr}"), getattr(meta, f"get_{attr}")
    setter(val)
    setattr(meta, attr, _static.List(getter()))

