
def test_ineq_avoid_wild_symbol_flip():
    # see issue #7951, we try to avoid this internally, e.g., by using
    # __lt__ instead of "<".
    from sympy.core.symbol import Wild
    p = symbols('p', cls=Wild)
    # x > p might flip, but Gt should not:
    assert Gt(x, p) == Gt(x, p, evaluate=False)
    # Previously failed as 'p > x':
    e = Lt(x, y).subs({y: p})
    assert e == Lt(x, p, evaluate=False)
    # Previously failed as 'p <= x':
    e = Ge(x, p).doit()
    assert e == Ge(x, p, evaluate=False)

