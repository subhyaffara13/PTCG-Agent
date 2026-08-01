
def test_evalf_default():
    from sympy.functions.special.gamma_functions import polygamma
    assert type(sin(4.0)) == Float
    assert type(re(sin(I + 1.0))) == Float
    assert type(im(sin(I + 1.0))) == Float
    assert type(sin(4)) == sin
    assert type(polygamma(2.0, 4.0)) == Float
    assert type(sin(Rational(1, 4))) == sin

