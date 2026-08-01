
def test_invalid_range():
    with pytest.raises(ValueError, match='2-length sequence'):
        ZoomFFT(100, [1, 2, 3])

