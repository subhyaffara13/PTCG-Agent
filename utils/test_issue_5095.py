
def test_issue_5095():
    f = Function('f')
    raises(ValueError, lambda: dsolve(f(x).diff(x)**2, f(x), 'fdsjf'))

