
def test_gh_22684():
    actual = signal.resample_poly(np.arange(2000, dtype=np.complex64), 6, 4)
    assert actual.dtype == np.complex64

