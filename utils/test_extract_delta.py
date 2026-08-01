
def test_extract_delta():
    raises(ValueError, lambda: _extract_delta(KD(i, j) + KD(k, l), i))

