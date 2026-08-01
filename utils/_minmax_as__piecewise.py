
def _minmax_as_Piecewise(op, *args):
    # helper for Min/Max rewrite as Piecewise
    from sympy.functions.elementary.piecewise import Piecewise
    ec = []
    for i, a in enumerate(args):
        c = [Relational(a, args[j], op) for j in range(i + 1, len(args))]
        ec.append((a, And(*c)))
    return Piecewise(*ec)

