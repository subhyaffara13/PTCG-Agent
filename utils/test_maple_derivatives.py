
def test_maple_derivatives():
    f = Function('f')
    assert maple_code(f(x).diff(x)) == 'diff(f(x), x)'
    assert maple_code(f(x).diff(x, 2)) == 'diff(f(x), x$2)'

