
def path_type(p: 'Path') -> str:
    """
    Find out what sort of thing a path is.
    """
    assert p.exists(), 'path does not exist'
    for method, name in path_types.items():
        if getattr(p, method)():
            return name

    return 'unknown'

