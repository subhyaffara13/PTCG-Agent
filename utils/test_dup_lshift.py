
def test_dup_lshift():
    assert dup_lshift([], 3, ZZ) == []
    assert dup_lshift([1], 3, ZZ) == [1, 0, 0, 0]

