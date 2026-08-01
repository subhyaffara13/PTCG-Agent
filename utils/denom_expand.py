
def denom_expand(expr, **hints):
    # default matches fraction's default
    a, b = fraction(expr, exact=hints.get('exact', False))
    return a / b.expand(denom=True, **hints)

