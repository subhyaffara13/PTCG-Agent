
def _mytype(f: Basic, x: Symbol) -> tuple[type[Basic], ...]:
    """ Create a hashable entity describing the type of f. """
    def key(x: type[Basic]) -> tuple[int, int, str]:
        return x.class_key()

    if x not in f.free_symbols:
        return ()
    elif f.is_Function:
        return type(f),
    return tuple(sorted((t for a in f.args for t in _mytype(a, x)), key=key))

