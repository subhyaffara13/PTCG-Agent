
def test_match_bug2():
    x, y = map(Symbol, 'xy')
    p, q, r = map(Wild, 'pqr')
    res = (x + y).match(p + q + r)
    assert (p + q + r).subs(res) == x + y

