
def test_basic_state():
    i, j, n, m = symbols('i,j,n,m')
    s = BosonState([0, 1, 2, 3, 4])
    assert len(s) == 5
    assert s.args[0] == tuple(range(5))
    assert s.up(0) == BosonState([1, 1, 2, 3, 4])
    assert s.down(4) == BosonState([0, 1, 2, 3, 3])
    for i in range(5):
        assert s.up(i).down(i) == s
    assert s.down(0) == 0
    for i in range(5):
        assert s[i] == i
    s = BosonState([n, m])
    assert s.down(0) == BosonState([n - 1, m])
    assert s.up(0) == BosonState([n + 1, m])

