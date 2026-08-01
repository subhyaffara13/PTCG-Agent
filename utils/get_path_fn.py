
def get_path_fn(path_type: str) -> PathSearchFunctionType:
    """Get the correct path finding function from str ``path_type``."""
    path_type = path_type.lower()
    if path_type not in _PATH_OPTIONS:
        raise KeyError(f"Path optimizer '{path_type}' not found, valid options are {set(_PATH_OPTIONS.keys())}.")

    return _PATH_OPTIONS[path_type]

