
def test_dup_rshift():
    assert dup_rshift([], 3, ZZ) == []
    assert dup_rshift([1, 0, 0, 0], 3, ZZ) == [1]

