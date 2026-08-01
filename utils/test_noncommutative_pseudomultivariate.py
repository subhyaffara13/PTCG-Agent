
def test_noncommutative_pseudomultivariate():
    # apart doesn't go inside noncommutative expressions
    class foo(Expr):
        is_commutative=False
    e = x/(x + x*y)
    c = 1/(1 + y)
    assert apart(e + foo(e)) == c + foo(c)
    assert apart(e*foo(e)) == c*foo(c)

