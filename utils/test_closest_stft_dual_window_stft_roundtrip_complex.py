
def test_closest_STFT_dual_window_STFT_roundtrip_complex(scaled):
    """STFT Roundtrip correctness of closest dual window with complex values. """
    np.random.seed(34905436)
    n, m_num, hop = 15, 7, 3
    win = 1j*hamming(m_num) + nuttall(m_num)
    desires_dual = 1j*triang(m_num) + blackman(m_num)
    dual, s = closest_STFT_dual_window(win, hop, desires_dual, scaled=scaled)

    SFT = ShortTimeFFT(win, hop=hop, dual_win=dual, fs=1, fft_mode='twosided',
                       scale_to=None, phase_shift=None)
    x = 10 * np.random.randn(n) + 10j * np.random.randn(n)
    Sx = SFT.stft(x)
    y = SFT.istft(Sx, 0, n)

    atol = np.finfo(win.dtype).resolution * 10
    xp_assert_close(y, x, atol=atol, err_msg=f"Invalid complex closest window ({s=})")

