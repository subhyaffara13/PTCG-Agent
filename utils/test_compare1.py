
def test_compare1():
    assert compare(2, x, x) == "<"
    assert compare(x, exp(x), x) == "<"
    assert compare(exp(x), exp(x**2), x) == "<"
    assert compare(exp(x**2), exp(exp(x)), x) == "<"
    assert compare(1, exp(exp(x)), x) == "<"

    assert compare(x, 2, x) == ">"
    assert compare(exp(x), x, x) == ">"
    assert compare(exp(x**2), exp(x), x) == ">"
    assert compare(exp(exp(x)), exp(x**2), x) == ">"
    assert compare(exp(exp(x)), 1, x) == ">"

    assert compare(2, 3, x) == "="
    assert compare(3, -5, x) == "="
    assert compare(2, -5, x) == "="

    assert compare(x, x**2, x) == "="
    assert compare(x**2, x**3, x) == "="
    assert compare(x**3, 1/x, x) == "="
    assert compare(1/x, x**m, x) == "="
    assert compare(x**m, -x, x) == "="

    assert compare(exp(x), exp(-x), x) == "="
    assert compare(exp(-x), exp(2*x), x) == "="
    assert compare(exp(2*x), exp(x)**2, x) == "="
    assert compare(exp(x)**2, exp(x + exp(-x)), x) == "="
    assert compare(exp(x), exp(x + exp(-x)), x) == "="

    assert compare(exp(x**2), 1/exp(x**2), x) == "="

