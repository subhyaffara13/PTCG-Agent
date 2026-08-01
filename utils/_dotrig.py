
def _dotrig(a, b):
    """Helper to tell whether ``a`` and ``b`` have the same sorts
    of symbols in them -- no need to test hyperbolic patterns against
    expressions that have no hyperbolics in them."""
    return a.func == b.func and (
        a.has(TrigonometricFunction) and b.has(TrigonometricFunction) or
        a.has(HyperbolicFunction) and b.has(HyperbolicFunction))

