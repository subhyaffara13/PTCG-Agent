
def recursive_subclasses(cls):
    """Yield *cls* and direct and indirect subclasses of *cls*."""
    yield cls
    for subcls in cls.__subclasses__():
        yield from recursive_subclasses(subcls)

