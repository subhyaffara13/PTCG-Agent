
def test_closest_STFT_dual_window_STFT_roundtrip(scaled):
    """STFT Roundtrip correctness of closest dual window. """
    np.random.seed(5613830)
    n, m_num, hop = 15, 7, 3
    w, desires_dual = hamming(m_num), triang(m_num)
    d, _ = closest_STFT_dual_window(w, hop, desires_dual, scaled=scaled)

    SFT = ShortTimeFFT(w, hop=hop, dual_win=d, fs=1, scale_to=None, phase_shift=None)
    x = 10 * np.random.randn(n)
    Sx = SFT.stft(x)
    y = SFT.istft(Sx, 0, n)

    atol = np.finfo(w.dtype).resolution * 10
    xp_assert_close(y, x, atol=atol, err_msg="Invalid closest window")

