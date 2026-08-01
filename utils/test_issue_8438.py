
def test_issue_8438():
    p = Poly([1, y, -2, -3], x).as_expr()
    roots = roots_cubic(Poly(p, x), x)
    z = Rational(-3, 2) - I*7/2  # this will fail in code given in commit msg
    post = [r.subs(y, z) for r in roots]
    assert set(post) == \
    set(roots_cubic(Poly(p.subs(y, z), x)))
    # /!\ if p is not made an expression, this is *very* slow
    assert all(p.subs({y: z, x: i}).n(2, chop=True) == 0 for i in post)

