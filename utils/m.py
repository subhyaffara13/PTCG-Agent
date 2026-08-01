
def m():
    """
    Fixture providing a memory filesystem.
    """
    m = fsspec.filesystem("memory")
    m.store.clear()
    m.pseudo_dirs.clear()
    m.pseudo_dirs.append("")
    try:
        yield m
    finally:
        m.store.clear()
        m.pseudo_dirs.clear()
        m.pseudo_dirs.append("")


def m():
    return 5

