
def reads_json(nbjson, **kwargs):
    """DEPRECATED, use reads"""
    warnings.warn(
        "reads_json is deprecated since nbformat 3.0, use reads",
        DeprecationWarning,
        stacklevel=2,
    )
    return reads(nbjson)

