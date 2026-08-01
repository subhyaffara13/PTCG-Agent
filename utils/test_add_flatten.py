
def test_add_flatten():
    # see https://github.com/sympy/sympy/issues/2633#issuecomment-29545524
    a = oo + I*oo
    b = oo - I*oo
    assert a + b is nan
    assert a - b is nan
    # FIXME: This evaluates as:
    #   >>> 1/a
    #   0*(oo + oo*I)
    # which should not simplify to 0. Should be fixed in Pow.eval
    #assert (1/a).simplify() == (1/b).simplify() == 0

    a = Pow(2, 3, evaluate=False)
    assert a + a == 16

