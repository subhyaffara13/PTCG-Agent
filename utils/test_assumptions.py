
def test_assumptions():
    rl = rewriterule(x + y, x**y, [x, y], assume=Q.integer(x))

    a, b = map(Symbol, 'ab')
    expr = a + b
    assert list(rl(expr, Q.integer(b))) == [b**a]


def test_assumptions():
    """
    Test whether diophantine respects the assumptions.
    """
    #Test case taken from the below so question regarding assumptions in diophantine module
    #https://stackoverflow.com/questions/23301941/how-can-i-declare-natural-symbols-with-sympy
    m, n = symbols('m n', integer=True, positive=True)
    diof = diophantine(n**2 + m*n - 500)
    assert diof == {(5, 20), (40, 10), (95, 5), (121, 4), (248, 2), (499, 1)}

    a, b = symbols('a b', integer=True, positive=False)
    diof = diophantine(a*b + 2*a + 3*b - 6)
    assert diof == {(-15, -3), (-9, -4), (-7, -5), (-6, -6), (-5, -8), (-4, -14)}

    x, y = symbols('x y', integer=True)
    diof = diophantine(10*x**2 + 5*x*y - 3*y)
    assert diof == {(1, -5), (-3, 5), (0, 0)}

    x, y = symbols('x y', integer=True, positive=True)
    diof = diophantine(10*x**2 + 5*x*y - 3*y)
    assert diof == set()

    x, y = symbols('x y', integer=True, negative=False)
    diof = diophantine(10*x**2 + 5*x*y - 3*y)
    assert diof == {(0, 0)}

