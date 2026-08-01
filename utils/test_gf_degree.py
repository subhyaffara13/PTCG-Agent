
def test_gf_degree():
    assert gf_degree([]) == -1
    assert gf_degree([1]) == 0
    assert gf_degree([1, 0]) == 1
    assert gf_degree([1, 0, 0, 0, 1]) == 4

