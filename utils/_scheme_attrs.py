
def _scheme_attrs(scheme):
    """Resolve install directories by applying the install schemes."""
    return {f'install_{key}': scheme[key] for key in SCHEME_KEYS}

