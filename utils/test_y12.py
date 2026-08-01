
def test_Y12():
    # => 2^(s - 4) gamma(s/2)/gamma(4 - s/2)   (0 < Re s < 1)
    # [Gradshteyn and Ryzhik 17.43(16)]
    x, s = symbols('x s')
    # returns Wrong value -2**(s - 4)*gamma(s/2 - 3)/gamma(-s/2 + 1)
    # https://github.com/sympy/sympy/issues/7182
    F, _, _ = mellin_transform(besselj(3, x)/x**3, x, s)
    assert F == -2**(s - 4)*gamma(s/2)/gamma(-s/2 + 4)

