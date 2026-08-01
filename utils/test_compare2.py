
def test_compare2():
    assert compare(exp(x), x**5, x) == ">"
    assert compare(exp(x**2), exp(x)**2, x) == ">"
    assert compare(exp(x), exp(x + exp(-x)), x) == "="
    assert compare(exp(x + exp(-x)), exp(x), x) == "="
    assert compare(exp(x + exp(-x)), exp(-x), x) == "="
    assert compare(exp(-x), x, x) == ">"
    assert compare(x, exp(-x), x) == "<"
    assert compare(exp(x + 1/x), x, x) == ">"
    assert compare(exp(-exp(x)), exp(x), x) == ">"
    assert compare(exp(exp(-exp(x)) + x), exp(-exp(x)), x) == "<"

