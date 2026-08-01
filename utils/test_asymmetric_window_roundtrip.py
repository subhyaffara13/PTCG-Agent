
def test_asymmetric_window_roundtrip(hop: int):
    """An asymmetric window could uncover indexing problems. """
    np.random.seed(23371)

    w = np.arange(16) / 8  # must be of type float
    w[len(w)//2:] = 1
    SFT = ShortTimeFFT(w, hop, fs=1)

    x = 10 * np.random.randn(64)
    Sx = SFT.stft(x)
    x1 = SFT.istft(Sx, k1=len(x))
    xp_assert_close(x1, x1, err_msg="Roundtrip for asymmetric window with " +
                                    f" {hop=} failed!")

