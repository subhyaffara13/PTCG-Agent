
def test_mul_pow_derivative():
    assert integrate(x*sec(x)*tan(x)) == x*sec(x) - log(tan(x) + sec(x))
    assert integrate(x*sec(x)**2, x) == x*tan(x) + log(cos(x))
    assert integrate(x**3*Derivative(f(x), (x, 4))) == \
           x**3*Derivative(f(x), (x, 3)) - 3*x**2*Derivative(f(x), (x, 2)) + 6*x*Derivative(f(x), x) - 6*f(x)


def test_mul_pow_derivative():
    assert_is_integral_of(x*sec(x)*tan(x), x*sec(x) - log(tan(x) + sec(x)))
    assert_is_integral_of(x*sec(x)**2, x*tan(x) + log(cos(x)))
    assert_is_integral_of(x**3*Derivative(f(x), (x, 4)),
                          x**3*Derivative(f(x), (x, 3)) - 3*x**2*Derivative(f(x), (x, 2)) +
                          6*x*Derivative(f(x), x) - 6*f(x))

