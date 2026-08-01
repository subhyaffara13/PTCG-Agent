
def test_irfft_with_n_1_regression():
    # Regression test for gh-25661
    x = np.arange(10)
    np.fft.irfft(x, n=1)
    np.fft.hfft(x, n=1)
    np.fft.irfft(np.array([0], complex), n=10)

