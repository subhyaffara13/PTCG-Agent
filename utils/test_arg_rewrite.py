
def test_arg_rewrite():
    assert arg(1 + I) == atan2(1, 1)

    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    assert arg(x + I*y).rewrite(atan2) == atan2(y, x)

