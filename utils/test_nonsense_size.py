
def test_nonsense_size(size):
    # Numpy and Scipy fft() give ValueError for 0 output size, so we do, too
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        CZT(size, 3)
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        ZoomFFT(size, 0.2, 3)
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        CZT(3, size)
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        ZoomFFT(3, 0.2, size)
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        czt([1, 2, 3], size)
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        zoom_fft([1, 2, 3], 0.2, size)

