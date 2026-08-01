
def test_spectrogram():
    """Verify spectrogram and cross-spectrogram methods. """
    SFT = ShortTimeFFT(np.ones(8), hop=4, fs=1)
    x, y = np.ones(10), np.arange(10)
    X, Y = SFT.stft(x), SFT.stft(y)
    xp_assert_close(SFT.spectrogram(x), X.real**2+X.imag**2)
    xp_assert_close(SFT.spectrogram(x, y), X * Y.conj())

