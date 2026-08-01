
def test_nan_extractions():
    for r in (1, 0, I, nan):
        assert nan.extract_additively(r) is None
        assert nan.extract_multiplicatively(r) is None

