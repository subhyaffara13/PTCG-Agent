
def test_piecewise_integrate2():
    from itertools import permutations
    lim = Tuple(x, c, d)
    p = Piecewise((1, x < a), (2, x > b), (3, True))
    q = p.integrate(lim)
    assert q == Piecewise(
        (-c + 2*d - 2*Min(d, Max(a, c)) + Min(d, Max(a, b, c)), c < d),
        (-2*c + d + 2*Min(c, Max(a, d)) - Min(c, Max(a, b, d)), True))
    for v in permutations((1, 2, 3, 4)):
        r = dict(zip((a, b, c, d), v))
        assert p.subs(r).integrate(lim.subs(r)) == q.subs(r)

