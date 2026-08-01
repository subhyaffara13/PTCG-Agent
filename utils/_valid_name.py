
def _valid_name(path: StrPath) -> bool:
    # Ignore invalid names that cannot be imported directly
    return os.path.basename(path).isidentifier()

