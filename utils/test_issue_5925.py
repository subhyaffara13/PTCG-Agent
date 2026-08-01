
def test_issue_5925():
    sx = sqrt(x + z).series(z, 0, 1)
    sxy = sqrt(x + y + z).series(z, 0, 1)
    s1, s2 = sx.subs(x, x + y), sxy
    assert (s1 - s2).expand().removeO().simplify() == 0

    sx = sqrt(x + z).series(z, 0, 1)
    sxy = sqrt(x + y + z).series(z, 0, 1)
    assert sxy.subs({x:1, y:2}) == sx.subs(x, 3)

