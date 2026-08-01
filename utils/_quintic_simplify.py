
def _quintic_simplify(expr):
    from sympy.simplify.simplify import powsimp
    expr = powsimp(expr)
    expr = cancel(expr)
    return together(expr)

