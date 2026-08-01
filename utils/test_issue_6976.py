
def test_issue_6976():
    x, y = symbols('x y')
    assert (sqrt(x)**3 + sqrt(x) + x + x**2).subs(sqrt(x), y) == \
        y**4 + y**3 + y**2 + y
    assert (x**4 + x**3 + x**2 + x + sqrt(x)).subs(x**2, y) == \
        sqrt(x) + x**3 + x + y**2 + y
    assert x.subs(x**3, y) == x
    assert x.subs(x**Rational(1, 3), y) == y**3

    # More substitutions are possible with nonnegative symbols
    x, y = symbols('x y', nonnegative=True)
    assert (x**4 + x**3 + x**2 + x + sqrt(x)).subs(x**2, y) == \
        y**Rational(1, 4) + y**Rational(3, 2) + sqrt(y) + y**2 + y
    assert x.subs(x**3, y) == y**Rational(1, 3)

