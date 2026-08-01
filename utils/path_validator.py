
def path_validator(v: Any) -> Path:
    if isinstance(v, Path):
        return v

    try:
        return Path(v)
    except TypeError:
        raise errors.PathError()

