
def test_get_indices_Pow():
    x = IndexedBase('x')
    y = IndexedBase('y')
    A = IndexedBase('A')
    i, j, k = Idx('i'), Idx('j'), Idx('k')
    assert get_indices(Pow(x[i], y[j])) == ({i, j}, {})
    assert get_indices(Pow(x[i, k], y[j, k])) == ({i, j, k}, {})
    assert get_indices(Pow(A[i, k], y[k] + A[k, j]*x[j])) == ({i, k}, {})
    assert get_indices(Pow(2, x[i])) == get_indices(exp(x[i]))

    # test of a design decision, this may change:
    assert get_indices(Pow(x[i], 2)) == ({i}, {})

