
def _is_analytic(f, x):
    """ Check if f(x), when expressed using G functions on the positive reals,
        will in fact agree with the G functions almost everywhere """
    return not any(x in expr.free_symbols for expr in f.atoms(Heaviside, Abs))

