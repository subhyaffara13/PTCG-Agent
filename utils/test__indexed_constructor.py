
def test_Indexed_constructor():
    i, j = symbols('i j', integer=True)
    A = Indexed('A', i, j)
    assert A == Indexed(Symbol('A'), i, j)
    assert A == Indexed(IndexedBase('A'), i, j)
    raises(TypeError, lambda: Indexed(A, i, j))
    raises(IndexException, lambda: Indexed("A"))
    assert A.free_symbols == {A, A.base.label, i, j}

