
def test_issue_5217():
    s = Symbol('s')
    z = (1 - 2*x*x)
    w = (1 + 2*x*x)
    q = 2*x*x*2*y*y
    sub = {2*x*x: s}
    assert w.subs(sub) == 1 + s
    assert z.subs(sub) == 1 - s
    assert q == 4*x**2*y**2
    assert q.subs(sub) == 2*y**2*s

