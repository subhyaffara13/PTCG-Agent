
def test_issue_12587():
    # sort holes into intervals
    p = Piecewise((1, x > 4), (2, Not((x <= 3) & (x > -1))), (3, True))
    assert p.integrate((x, -5, 5)) == 23
    p = Piecewise((1, x > 1), (2, x < y), (3, True))
    lim = x, -3, 3
    ans = p.integrate(lim)
    for i in range(-1, 3):
        assert ans.subs(y, i) == p.subs(y, i).integrate(lim)

