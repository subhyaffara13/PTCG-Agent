
def test_Indexed_properties():
    i, j = symbols('i j', integer=True)
    A = Indexed('A', i, j)
    assert A.name == 'A[i, j]'
    assert A.rank == 2
    assert A.indices == (i, j)
    assert A.base == IndexedBase('A')
    assert A.ranges == [None, None]
    raises(IndexException, lambda: A.shape)

    n, m = symbols('n m', integer=True)
    assert Indexed('A', Idx(
        i, m), Idx(j, n)).ranges == [Tuple(0, m - 1), Tuple(0, n - 1)]
    assert Indexed('A', Idx(i, m), Idx(j, n)).shape == Tuple(m, n)
    raises(IndexException, lambda: Indexed("A", Idx(i, m), Idx(j)).shape)

