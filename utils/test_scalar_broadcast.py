
def test_scalar_broadcast():
    x = IndexedBase('x')
    y = IndexedBase('y')
    i, j = Idx('i'), Idx('j')
    assert get_indices(x[i] + y[i, i]) == ({i}, {})
    assert get_indices(x[i] + y[j, j]) == ({i}, {})

