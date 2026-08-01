
def test_manualintegrate_exponentials():
    assert manualintegrate(exp(2*x), x) == exp(2*x) / 2
    assert manualintegrate(2**x, x) == (2 ** x) / log(2)
    assert_is_integral_of(1/sqrt(1-exp(2*x)),
                          log(sqrt(1 - exp(2*x)) - 1)/2 - log(sqrt(1 - exp(2*x)) + 1)/2)

    assert manualintegrate(1 / x, x) == log(x)
    assert manualintegrate(1 / (2*x + 3), x) == log(2*x + 3) / 2
    assert manualintegrate(log(x)**2 / x, x) == log(x)**3 / 3

    assert_is_integral_of(x**x*(log(x)+1), x**x)

