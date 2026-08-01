
def test_issue_16146():
    raises(ValueError, lambda: dsolve([f(x).diff(x), g(x).diff(x)], [f(x), g(x), h(x)]))
    raises(ValueError, lambda: dsolve([f(x).diff(x), g(x).diff(x)], [f(x)]))

