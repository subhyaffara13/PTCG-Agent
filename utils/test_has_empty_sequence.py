
def test_has_empty_sequence():
    assert Sum(1, (x, 1, 1)).has_empty_sequence is False
    assert Sum(1, (x, 1, 9)).has_empty_sequence is False
    assert Sum(1, (x, 1, -9)).has_empty_sequence is False
    assert Sum(1, (x, 1, 0)).has_empty_sequence is True
    assert Sum(1, (x, y, y - 1)).has_empty_sequence is True
    assert Sum(1, (x, 3, 2), (y, -oo, oo)).has_empty_sequence is True
    assert Sum(1, (y, -oo, oo), (x, 3, 2)).has_empty_sequence is True
    assert Sum(1, (x, oo, oo)).has_empty_sequence is False

