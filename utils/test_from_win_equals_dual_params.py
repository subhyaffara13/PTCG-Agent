
def test_from_win_equals_dual_params(m, hop, fft_bins):
    """Test windows parameterizations for `ShortTimeFFT.from_closest_win_equals_dual`.

    The flattop window is used since it also has negative values.
    """
    desired_win = get_window('flattop', m, fftbins=fft_bins)
    SFT0 = ShortTimeFFT.from_win_equals_dual(desired_win, hop, fs=1)
    xp_assert_close(SFT0.dual_win, SFT0.win, err_msg="win must equals dual window!")

    SFT1 = ShortTimeFFT(SFT0.win, hop, fs=1)
    xp_assert_close(SFT1.dual_win, SFT0.win, err_msg="dual win isn't canonical win!")

