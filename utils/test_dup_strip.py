
def test_dup_strip():
    assert dup_strip([]) == []
    assert dup_strip([0]) == []
    assert dup_strip([0, 0, 0]) == []

    assert dup_strip([1]) == [1]
    assert dup_strip([0, 1]) == [1]
    assert dup_strip([0, 0, 0, 1]) == [1]

    assert dup_strip([1, 2, 0]) == [1, 2, 0]
    assert dup_strip([0, 1, 2, 0]) == [1, 2, 0]
    assert dup_strip([0, 0, 0, 1, 2, 0]) == [1, 2, 0]

