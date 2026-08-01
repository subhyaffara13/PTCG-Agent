
def test_function():
    f, l = map(Function, 'fl')
    x = Symbol('x')
    assert exp(l(x))*l(x)/exp(l(x)) == l(x)
    assert exp(f(x))*f(x)/exp(f(x)) == f(x)

