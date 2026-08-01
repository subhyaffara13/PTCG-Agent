
def test_dup_inflate():
    assert dup_inflate([], 17, ZZ) == []

    assert dup_inflate([1, 2, 3], 1, ZZ) == [1, 2, 3]
    assert dup_inflate([1, 2, 3], 2, ZZ) == [1, 0, 2, 0, 3]
    assert dup_inflate([1, 2, 3], 3, ZZ) == [1, 0, 0, 2, 0, 0, 3]
    assert dup_inflate([1, 2, 3], 4, ZZ) == [1, 0, 0, 0, 2, 0, 0, 0, 3]

    raises(IndexError, lambda: dup_inflate([1, 2, 3], 0, ZZ))

