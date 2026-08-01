
def _set_config(dist: Distribution, field: str, value: Any):
    val = _PREPROCESS.get(field, _noop)(dist, value)
    setter = getattr(dist.metadata, f"set_{field}", None)
    if setter:
        setter(val)
    elif hasattr(dist.metadata, field) or field in SETUPTOOLS_PATCHES:
        setattr(dist.metadata, field, val)
    else:
        setattr(dist, field, val)

