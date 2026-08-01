
def test_get_indices_add():
    x = IndexedBase('x')
    y = IndexedBase('y')
    A = IndexedBase('A')
    i, j, k = Idx('i'), Idx('j'), Idx('k')
    assert get_indices(x[i] + 2*y[i]) == ({i}, {})
    assert get_indices(y[i] + 2*A[i, j]*x[j]) == ({i}, {})
    assert get_indices(y[i] + 2*(x[i] + A[i, j]*x[j])) == ({i}, {})
    assert get_indices(y[i] + x[i]*(A[j, j] + 1)) == ({i}, {})
    assert get_indices(
        y[i] + x[i]*x[j]*(y[j] + A[j, k]*x[k])) == ({i}, {})

