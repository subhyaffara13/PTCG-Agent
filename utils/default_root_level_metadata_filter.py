
def default_root_level_metadata_filter(fmt):
    """Return defaults for settings that promote or demote root level metadata."""
    if fmt and fmt.get("format_name") == MYST_FORMAT_NAME:
        from .myst import _DEFAULT_ROOT_LEVEL_METADATA as default_filter
    else:
        default_filter = _DEFAULT_ROOT_LEVEL_METADATA
    return default_filter

