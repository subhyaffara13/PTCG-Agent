
def test_simple_6():
    assert Order(x) - Order(x) == Order(x)
    assert Order(x) + Order(1) == Order(1)
    assert Order(x) + Order(x**2) == Order(x)
    assert Order(1/x) + Order(1) == Order(1/x)
    assert Order(x) + Order(exp(1/x)) == Order(exp(1/x))
    assert Order(x**3) + Order(exp(2/x)) == Order(exp(2/x))
    assert Order(x**-3) + Order(exp(2/x)) == Order(exp(2/x))

