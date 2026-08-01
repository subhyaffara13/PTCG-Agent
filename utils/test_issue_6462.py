
def test_issue_6462():
    from sympy.core.symbol import Symbol
    x = Symbol('x')
    n = Symbol('n')
    # Not the actual issue, still wrong answer for n = 1, but that there is no
    # exception
    assert integrate(cos(x**n)/x**n, x, meijerg=True).subs(n, 2).equals(
            integrate(cos(x**2)/x**2, x, meijerg=True))

