
def test_dup_degree():
    assert ninf == float('-inf')
    assert dup_degree([]) is ninf
    assert dup_degree([1]) == 0
    assert dup_degree([1, 0]) == 1
    assert dup_degree([1, 0, 0, 0, 1]) == 4

