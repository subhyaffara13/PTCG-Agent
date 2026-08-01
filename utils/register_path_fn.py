
def register_path_fn(name: str, fn: PathSearchFunctionType) -> None:
    """Add path finding function ``fn`` as an option with ``name``."""
    if name in _PATH_OPTIONS:
        raise KeyError(f"Path optimizer '{name}' already exists.")

    _PATH_OPTIONS[name.lower()] = fn

