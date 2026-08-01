
def test_nested_pow():
    assert integrate(sqrt(x**2)) == x*sqrt(x**2)/2
    assert integrate(sqrt(x**(S(5)/3))) == 6*x*sqrt(x**(S(5)/3))/11
    assert integrate(1/sqrt(x**2)) == x*log(x)/sqrt(x**2)
    assert integrate(x*sqrt(x**(-4))) == x**2*sqrt(x**-4)*log(x)


def test_nested_pow():
    assert_is_integral_of(sqrt(x**2), x*sqrt(x**2)/2)
    assert_is_integral_of(sqrt(x**(S(5)/3)), 6*x*sqrt(x**(S(5)/3))/11)
    assert_is_integral_of(1/sqrt(x**2), x*log(x)/sqrt(x**2))
    assert_is_integral_of(x*sqrt(x**(-4)), x**2*sqrt(x**-4)*log(x))
    f = (c*(a+b*x)**d)**e
    F1 = (c*(a + b*x)**d)**e*(a/b + x)/(d*e + 1)
    F2 = (c*(a + b*x)**d)**e*(a/b + x)*log(a/b + x)
    assert manualintegrate(f, x) == \
        Piecewise((Piecewise((F1, Ne(d*e, -1)), (F2, True)), Ne(b, 0)), (x*(a**d*c)**e, True))
    assert F1.diff(x).equals(f)
    assert F2.diff(x).subs(d*e, -1).equals(f)

