
def test_cohere():
    N = 1024
    np.random.seed(19680801)
    x = np.random.randn(N)
    # phase offset
    y = np.roll(x, 20)
    # high-freq roll-off
    y = np.convolve(y, np.ones(20) / 20., mode='same')
    cohsq, f = mlab.cohere(x, y, NFFT=256, Fs=2, noverlap=128)
    assert_allclose(np.mean(cohsq), 0.837, atol=1.e-3)
    assert np.isreal(np.mean(cohsq))

