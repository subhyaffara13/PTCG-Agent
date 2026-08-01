
def test_get_indices_mul():
    x = IndexedBase('x')
    y = IndexedBase('y')
    i, j = Idx('i'), Idx('j')
    assert get_indices(x[j]*y[i]) == ({i, j}, {})
    assert get_indices(x[i]*y[j]) == ({i, j}, {})

