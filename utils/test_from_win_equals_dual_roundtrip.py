
def test_from_win_equals_dual_roundtrip(m, hop, fft_bins, scale_to):
    """Testing roundtrip verifies that the dual window is correct.
    """
    desired_win = get_window('flattop', m, fftbins=fft_bins)
    SFT0 = ShortTimeFFT.from_win_equals_dual(desired_win, hop, fs=1)

    x = np.cos(np.arange(2*m)**2)
    x1 = SFT0.istft(SFT0.stft(x), 0, len(x))
    xp_assert_close(x1, x, err_msg="Roundtrip for win equaling its dual failed!")

