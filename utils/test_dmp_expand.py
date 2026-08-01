
def test_dmp_expand():
    assert dmp_expand((), 1, ZZ) == [[1]]
    assert dmp_expand(([[1], [2], [3]], [[1], [2]], [[7], [5], [4], [3]]), 1, ZZ) == \
        dmp_mul([[1], [2], [3]], dmp_mul([[1], [2]], [[7], [5], [
                4], [3]], 1, ZZ), 1, ZZ)

