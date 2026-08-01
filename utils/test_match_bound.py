
def test_match_bound():
    V, W = map(Wild, "VW")
    x, y = symbols('x y')
    assert Sum(x, (x, 1, 2)).match(Sum(y, (y, 1, W))) is None
    assert Sum(x, (x, 1, 2)).match(Sum(V, (V, 1, W))) == {W: 2, V:x}
    assert Sum(x, (x, 1, 2)).match(Sum(V, (V, 1, 2))) == {V:x}

