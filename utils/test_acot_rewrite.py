
def test_acot_rewrite():
    assert acot(x).rewrite(log) == I*(log(1 - I/x)-log(1 + I/x))/2
    assert acot(x).rewrite(asin) == x*(-asin(sqrt(-x**2)/sqrt(-x**2 - 1)) + pi/2)*sqrt(x**(-2))
    assert acot(x).rewrite(acos) == x*sqrt(x**(-2))*acos(sqrt(-x**2)/sqrt(-x**2 - 1))
    assert acot(x).rewrite(atan) == atan(1/x)
    assert acot(x).rewrite(asec) == x*sqrt(x**(-2))*asec(sqrt((x**2 + 1)/x**2))
    assert acot(x).rewrite(acsc) == x*(-acsc(sqrt((x**2 + 1)/x**2)) + pi/2)*sqrt(x**(-2))

    assert acot(-I/5).evalf() == acot(x).rewrite(log).evalf(subs={x:-I/5})
    assert acot(I/5).evalf() == acot(x).rewrite(log).evalf(subs={x:I/5})

