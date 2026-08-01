
def test_linear_subs():
    from sympy.functions.special.bessel import besselj
    assert integrate(sin(x - 1), x, meijerg=True) == -cos(1 - x)
    assert integrate(besselj(1, x - 1), x, meijerg=True) == -besselj(0, 1 - x)

