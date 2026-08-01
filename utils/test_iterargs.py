
def test_iterargs():
    f = Function('f')
    x = symbols('x')
    assert list(iterfreeargs(Integral(f(x), (f(x), 1)))) == [
        Integral(f(x), (f(x), 1)), 1]
    assert list(iterargs(Integral(f(x), (f(x), 1)))) == [
        Integral(f(x), (f(x), 1)), f(x), (f(x), 1), x, f(x), 1, x]

