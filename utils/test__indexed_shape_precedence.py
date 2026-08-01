
def test_Indexed_shape_precedence():
    i, j = symbols('i j', integer=True)
    o, p = symbols('o p', integer=True)
    n, m = symbols('n m', integer=True)
    a = IndexedBase('a', shape=(o, p))
    assert a.shape == Tuple(o, p)
    assert Indexed(
        a, Idx(i, m), Idx(j, n)).ranges == [Tuple(0, m - 1), Tuple(0, n - 1)]
    assert Indexed(a, Idx(i, m), Idx(j, n)).shape == Tuple(o, p)
    assert Indexed(
        a, Idx(i, m), Idx(j)).ranges == [Tuple(0, m - 1), (None, None)]
    assert Indexed(a, Idx(i, m), Idx(j)).shape == Tuple(o, p)

