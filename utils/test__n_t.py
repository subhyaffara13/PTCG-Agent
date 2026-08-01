
def test__nT():
    assert [_nT(i, j) for i in range(5) for j in range(i + 2)] == [
            1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 2, 1, 1, 0]
    check = [_nT(10, i) for i in range(11)]
    assert check == [0, 1, 5, 8, 9, 7, 5, 3, 2, 1, 1]
    assert all(type(i) is int for i in check)
    assert _nT(10, 5) == 7
    assert _nT(100, 98) == 2
    assert _nT(100, 100) == 1
    assert _nT(10, 3) == 8

