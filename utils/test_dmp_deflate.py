
def test_dmp_deflate():
    assert dmp_deflate([[]], 1, ZZ) == ((1, 1), [[]])
    assert dmp_deflate([[2]], 1, ZZ) == ((1, 1), [[2]])

    f = [[1, 0, 0], [], [1, 0], [], [1]]

    assert dmp_deflate(f, 1, ZZ) == ((2, 1), [[1, 0, 0], [1, 0], [1]])

