
def test_atan_rewrite():
    assert atan(x).rewrite(log) == I*(log(1 - I*x)-log(1 + I*x))/2
    assert atan(x).rewrite(asin) == (-asin(1/sqrt(x**2 + 1)) + pi/2)*sqrt(x**2)/x
    assert atan(x).rewrite(acos) == sqrt(x**2)*acos(1/sqrt(x**2 + 1))/x
    assert atan(x).rewrite(acot) == acot(1/x)
    assert atan(x).rewrite(asec) == sqrt(x**2)*asec(sqrt(x**2 + 1))/x
    assert atan(x).rewrite(acsc) == (-acsc(sqrt(x**2 + 1)) + pi/2)*sqrt(x**2)/x

    assert atan(-5*I).evalf() == atan(x).rewrite(log).evalf(subs={x:-5*I})
    assert atan(5*I).evalf() == atan(x).rewrite(log).evalf(subs={x:5*I})

