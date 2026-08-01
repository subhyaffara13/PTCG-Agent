
def test_runs():
    assert runs([]) == []
    assert runs([1]) == [[1]]
    assert runs([1, 1]) == [[1], [1]]
    assert runs([1, 1, 2]) == [[1], [1, 2]]
    assert runs([1, 2, 1]) == [[1, 2], [1]]
    assert runs([2, 1, 1]) == [[2], [1], [1]]
    from operator import lt
    assert runs([2, 1, 1], lt) == [[2, 1], [1]]

