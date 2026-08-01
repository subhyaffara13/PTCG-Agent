
def test_expbug4():
    x = Symbol("x", real=True)
    assert (log(
        sin(2*x)/x)*(1 + x)).series(x, 0, 2) == log(2) + x*log(2) + O(x**2, x)
    assert exp(
        log(sin(2*x)/x)*(1 + x)).series(x, 0, 2) == 2 + 2*x*log(2) + O(x**2)

    assert exp(log(2) + O(x)).nseries(x, 0, 2) == 2 + O(x)
    assert ((2 + O(x))**(1 + x)).nseries(x, 0, 2) == 2 + O(x)

