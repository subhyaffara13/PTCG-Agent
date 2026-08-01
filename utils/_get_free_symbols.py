
def _get_free_symbols(exprs):
    """Returns the free symbols of a symbolic expression.

    If the expression contains any of these elements, assume that they are
    the "free symbols" of the expression:

    * indexed objects
    * applied undefined function (useful for sympy.physics.mechanics module)
    """
    if not isinstance(exprs, (list, tuple, set)):
        exprs = [exprs]
    if all(callable(e) for e in exprs):
        return set()

    free = set().union(*[e.atoms(Indexed) for e in exprs])
    free = free.union(*[e.atoms(AppliedUndef) for e in exprs])
    return free or set().union(*[e.free_symbols for e in exprs])

