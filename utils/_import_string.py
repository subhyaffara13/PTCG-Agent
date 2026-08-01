
def _import_string(names: list[tuple[str, str | None]]) -> str:
    """return a list of (name, asname) formatted as a string"""
    _names = []
    for name, asname in names:
        if asname is not None:
            _names.append(f"{name} as {asname}")
        else:
            _names.append(name)
    return ", ".join(_names)

