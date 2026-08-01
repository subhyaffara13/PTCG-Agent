
def test_get_indices_Idx():
    f = Function('f')
    i, j = Idx('i'), Idx('j')
    assert get_indices(f(i)*j) == ({i, j}, {})
    assert get_indices(f(j, i)) == ({j, i}, {})
    assert get_indices(f(i)*i) == (set(), {})

