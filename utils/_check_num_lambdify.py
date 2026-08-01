
def _check_num_lambdify(expr, opt, val_subs, approx_ref, lambdify_kw=None, poorness=1e10):
    """ poorness=1e10 signifies that `expr` loses precision of at least ten decimal digits. """
    num_ref = expr.subs(val_subs).evalf()
    eps = numpy.finfo(numpy.float64).eps
    assert abs(num_ref - approx_ref) < approx_ref*eps
    f1 = lambdify(list(val_subs.keys()), opt, **(lambdify_kw or {}))
    args_float = tuple(map(float, val_subs.values()))
    num_err1 = abs(f1(*args_float) - approx_ref)
    assert num_err1 < abs(num_ref*eps)
    f2 = lambdify(list(val_subs.keys()), expr, **(lambdify_kw or {}))
    num_err2 = abs(f2(*args_float) - approx_ref)
    assert num_err2 > abs(num_ref*eps*poorness)   # this only ensures that the *test* works as intended

