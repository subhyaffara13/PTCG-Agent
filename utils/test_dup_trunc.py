
def test_dup_trunc():
    assert dup_trunc([1, 2, 3, 4, 5, 6], ZZ(3), ZZ) == [1, -1, 0, 1, -1, 0]
    assert dup_trunc([6, 5, 4, 3, 2, 1], ZZ(3), ZZ) == [-1, 1, 0, -1, 1]

    R = ZZ_I
    assert dup_trunc([R(3), R(4), R(5)], R(3), R) == [R(1), R(-1)]

    K = FF(5)
    assert dup_trunc([K(3), K(4), K(5)], K(3), K) == [K(1), K(0)]

