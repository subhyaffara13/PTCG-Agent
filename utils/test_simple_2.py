
def test_simple_2():
    assert Order(2*x)*x == Order(x**2)
    assert Order(2*x)/x == Order(1, x)
    assert Order(2*x)*x*exp(1/x) == Order(x**2*exp(1/x))
    assert (Order(2*x)*x*exp(1/x)/log(x)**3).expr == x**2*exp(1/x)*log(x)**-3

