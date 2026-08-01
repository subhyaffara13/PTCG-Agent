
def _sympy_ite(a: sympy.Basic, t: sympy.Basic, f: sympy.Basic) -> sympy.Basic:
    import sympy

    return sympy.Piecewise((t, a), (f, True))

