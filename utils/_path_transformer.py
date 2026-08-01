
def _path_transformer(value: str) -> str:
    """Expand user and variables in a path."""
    return os.path.expandvars(os.path.expanduser(value))

