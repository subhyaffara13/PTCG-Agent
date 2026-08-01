
def plot_polynomial(expr):
    """Plots the polynomial using the functions written in
    plotting module which in turn uses matplotlib backend.

    Parameter
    =========

    expr:
        Denotes a polynomial(SymPy expression).
    """
    from sympy.plotting.plot import plot3d, plot
    gens = expr.free_symbols
    if len(gens) == 2:
        plot3d(expr)
    else:
        plot(expr)

