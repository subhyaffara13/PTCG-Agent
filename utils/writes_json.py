
def writes_json(nb, **kwargs):
    """DEPRECATED, use writes"""
    warnings.warn(
        "writes_json is deprecated since nbformat 3.0, use writes",
        DeprecationWarning,
        stacklevel=2,
    )
    return writes(nb, **kwargs)

