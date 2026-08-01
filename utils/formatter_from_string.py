
def formatter_from_string(name: str) -> Callable[..., str]:
    return _wrap_modes.get(name.upper(), grid)

