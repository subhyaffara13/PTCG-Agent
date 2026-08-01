
def test_x_minus_y_not_same_as_x_lt_y():
    """
    A consequence of pull request #7792 is that `x - y < 0` and `x < y`
    are not synonymous.
    """
    x = I + 2
    y = I + 3
    raises(TypeError, lambda: x < y)
    assert x - y < 0

    ineq = Lt(x, y, evaluate=False)
    raises(TypeError, lambda: ineq.doit())
    assert ineq.lhs - ineq.rhs < 0

    t = Symbol('t', imaginary=True)
    x = 2 + t
    y = 3 + t
    ineq = Lt(x, y, evaluate=False)
    raises(TypeError, lambda: ineq.doit())
    assert ineq.lhs - ineq.rhs < 0

    # this one should give error either way
    x = I + 2
    y = 2*I + 3
    raises(TypeError, lambda: x < y)
    raises(TypeError, lambda: x - y < 0)

