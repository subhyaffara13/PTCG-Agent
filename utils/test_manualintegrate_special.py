
def test_manualintegrate_special():
    f, F = 4*exp(-x**2/3), 2*sqrt(3)*sqrt(pi)*erf(sqrt(3)*x/3)
    assert_is_integral_of(f, F)
    f, F = 3*exp(4*x**2), 3*sqrt(pi)*erfi(2*x)/4
    assert_is_integral_of(f, F)
    f, F = x**Rational(1, 3)*exp(-x/8), -16*uppergamma(Rational(4, 3), x/8)
    assert_is_integral_of(f, F)
    f, F = exp(2*x)/x, Ei(2*x)
    assert_is_integral_of(f, F)
    f, F = exp(1 + 2*x - x**2), sqrt(pi)*exp(2)*erf(x - 1)/2
    assert_is_integral_of(f, F)
    f = sin(x**2 + 4*x + 1)
    F = (sqrt(2)*sqrt(pi)*(-sin(3)*fresnelc(sqrt(2)*(2*x + 4)/(2*sqrt(pi))) +
        cos(3)*fresnels(sqrt(2)*(2*x + 4)/(2*sqrt(pi))))/2)
    assert_is_integral_of(f, F)
    f, F = cos(4*x**2), sqrt(2)*sqrt(pi)*fresnelc(2*sqrt(2)*x/sqrt(pi))/4
    assert_is_integral_of(f, F)
    f, F = sin(3*x + 2)/x, sin(2)*Ci(3*x) + cos(2)*Si(3*x)
    assert_is_integral_of(f, F)
    f, F = sinh(3*x - 2)/x, -sinh(2)*Chi(3*x) + cosh(2)*Shi(3*x)
    assert_is_integral_of(f, F)
    f, F = 5*cos(2*x - 3)/x, 5*cos(3)*Ci(2*x) + 5*sin(3)*Si(2*x)
    assert_is_integral_of(f, F)
    f, F = cosh(x/2)/x, Chi(x/2)
    assert_is_integral_of(f, F)
    f, F = cos(x**2)/x, Ci(x**2)/2
    assert_is_integral_of(f, F)
    f, F = 1/log(2*x + 1), li(2*x + 1)/2
    assert_is_integral_of(f, F)
    f, F = polylog(2, 5*x)/x, polylog(3, 5*x)
    assert_is_integral_of(f, F)
    f, F = 5/sqrt(3 - 2*sin(x)**2), 5*sqrt(3)*elliptic_f(x, Rational(2, 3))/3
    assert_is_integral_of(f, F)
    f, F = sqrt(4 + 9*sin(x)**2), 2*elliptic_e(x, Rational(-9, 4))
    assert_is_integral_of(f, F)

