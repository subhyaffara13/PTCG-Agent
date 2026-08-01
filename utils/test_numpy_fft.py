
def test_numpy_fft():
    bad_results = check_dir(np.fft)
    assert bad_results == {}

