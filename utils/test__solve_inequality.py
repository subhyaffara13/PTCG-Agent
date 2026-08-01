
def test__solve_inequality():
    for op in (Gt, Lt, Le, Ge, Eq, Ne):
        assert _solve_inequality(op(x, 1), x).lhs == x
        assert _solve_inequality(op(S.One, x), x).lhs == x
    # don't get tricked by symbol on right: solve it
    assert _solve_inequality(Eq(2*x - 1, x), x) == Eq(x, 1)
    ie = Eq(S.One, y)
    assert _solve_inequality(ie, x) == ie
    for fx in (x**2, exp(x), sin(x) + cos(x), x*(1 + x)):
        for c in (0, 1):
            e = 2*fx - c > 0
            assert _solve_inequality(e, x, linear=True) == (
                fx > c/S(2))
    assert _solve_inequality(2*x**2 + 2*x - 1 < 0, x, linear=True) == (
        x*(x + 1) < S.Half)
    assert _solve_inequality(Eq(x*y, 1), x) == Eq(x*y, 1)
    nz = Symbol('nz', nonzero=True)
    assert _solve_inequality(Eq(x*nz, 1), x) == Eq(x, 1/nz)
    assert _solve_inequality(x*nz < 1, x) == (x*nz < 1)
    a = Symbol('a', positive=True)
    assert _solve_inequality(a/x > 1, x) == (S.Zero < x) & (x < a)
    assert _solve_inequality(a/x > 1, x, linear=True) == (1/x > 1/a)
    # make sure to include conditions under which solution is valid
    e = Eq(1 - x, x*(1/x - 1))
    assert _solve_inequality(e, x) == Ne(x, 0)
    assert _solve_inequality(x < x*(1/x - 1), x) == (x < S.Half) & Ne(x, 0)

