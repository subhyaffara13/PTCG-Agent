
def test_indexed_is_constant():
    A = IndexedBase("A")
    i, j, k = symbols("i,j,k")
    assert not A[i].is_constant()
    assert A[i].is_constant(j)
    assert not A[1+2*i, k].is_constant()
    assert not A[1+2*i, k].is_constant(i)
    assert A[1+2*i, k].is_constant(j)
    assert not A[1+2*i, k].is_constant(k)

