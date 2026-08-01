
def test_issue_6052():
    G = meijerg((), (), (1,), (0,), -x)
    g = hyperexpand(G)
    assert limit(g, x, 0, '+-') == 0
    assert limit(g, x, oo) == -oo

