
def test_dup_expand():
    assert dup_expand((), ZZ) == [1]
    assert dup_expand(([1, 2, 3], [1, 2], [7, 5, 4, 3]), ZZ) == \
        dup_mul([1, 2, 3], dup_mul([1, 2], [7, 5, 4, 3], ZZ), ZZ)

