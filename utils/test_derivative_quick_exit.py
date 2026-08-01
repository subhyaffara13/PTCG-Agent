
def test_derivative_quick_exit():
    assert f(x).diff(y) == 0
    assert f(x).diff(y, f(x)) == 0
    assert f(x).diff(x, f(y)) == 0
    assert f(f(x)).diff(x, f(x), f(y)) == 0
    assert f(f(x)).diff(x, f(x), y) == 0
    assert f(x).diff(g(x)) == 0
    assert f(x).diff(x, f(x).diff(x)) == 1
    df = f(x).diff(x)
    assert f(x).diff(df) == 0
    dg = g(x).diff(x)
    assert dg.diff(df).doit() == 0

