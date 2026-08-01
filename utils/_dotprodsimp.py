
def _dotprodsimp(expr, withsimp=False):
    """Wrapper for simplify.dotprodsimp to avoid circular imports."""
    from sympy.simplify.simplify import dotprodsimp as dps
    return dps(expr, withsimp=withsimp)

