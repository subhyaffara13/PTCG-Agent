
def test_is_HNF():
    M = DM([
        [3, 2, 1],
        [0, 2, 1],
        [0, 0, 1]
    ], ZZ)
    M1 = DM([
        [3, 2, 1],
        [0, -2, 1],
        [0, 0, 1]
    ], ZZ)
    M2 = DM([
        [3, 2, 3],
        [0, 2, 1],
        [0, 0, 1]
    ], ZZ)
    assert is_sq_maxrank_HNF(M) is True
    assert is_sq_maxrank_HNF(M1) is False
    assert is_sq_maxrank_HNF(M2) is False

