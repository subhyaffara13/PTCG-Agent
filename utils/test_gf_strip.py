
def test_gf_strip():
    assert gf_strip([]) == []
    assert gf_strip([0]) == []
    assert gf_strip([0, 0, 0]) == []

    assert gf_strip([1]) == [1]
    assert gf_strip([0, 1]) == [1]
    assert gf_strip([0, 0, 0, 1]) == [1]

    assert gf_strip([1, 2, 0]) == [1, 2, 0]
    assert gf_strip([0, 1, 2, 0]) == [1, 2, 0]
    assert gf_strip([0, 0, 0, 1, 2, 0]) == [1, 2, 0]

