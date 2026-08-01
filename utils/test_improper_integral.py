
def test_improper_integral():
    assert integrate(log(x), (x, 0, 1)) == -1
    assert integrate(x**(-2), (x, 1, oo)) == 1
    assert integrate(1/(1 + exp(x)), (x, 0, oo)) == log(2)

