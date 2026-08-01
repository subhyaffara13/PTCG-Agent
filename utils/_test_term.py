
def _test_term(coeff, func, order):
    r"""
    Linear Euler ODEs have the form  K*x**order*diff(y(x), x, order) = F(x),
    where K is independent of x and y(x), order>= 0.
    So we need to check that for each term, coeff == K*x**order from
    some K.  We have a few cases, since coeff may have several
    different types.
    """
    x = func.args[0]
    f = func.func
    if order < 0:
        raise ValueError("order should be greater than 0")
    if coeff == 0:
        return True
    if order == 0:
        if x in coeff.free_symbols:
            return False
        return True
    if coeff.is_Mul:
        if coeff.has(f(x)):
            return False
        return x**order in coeff.args
    elif coeff.is_Pow:
        return coeff.as_base_exp() == (x, order)
    elif order == 1:
        return x == coeff
    return False

