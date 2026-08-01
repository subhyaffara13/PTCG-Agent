
def test_rcode_functions():
    assert rcode(sin(x) ** cos(x)) == "sin(x)^cos(x)"
    assert rcode(factorial(x) + gamma(y)) == "factorial(x) + gamma(y)"
    assert rcode(beta(Min(x, y), Max(x, y))) == "beta(min(x, y), max(x, y))"

