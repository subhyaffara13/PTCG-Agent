
def test_get_indices_Indexed():
    x = IndexedBase('x')
    i, j = Idx('i'), Idx('j')
    assert get_indices(x[i, j]) == ({i, j}, {})
    assert get_indices(x[j, i]) == ({j, i}, {})

