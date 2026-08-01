
def test_issue_17988():
    x = Symbol('x')
    p = poly(x - 1)
    with warns_deprecated_sympy():
        M = Matrix([[poly(x + 1), poly(x + 1)]])
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        assert p * M == M * p == Matrix([[poly(x**2 - 1), poly(x**2 - 1)]])

