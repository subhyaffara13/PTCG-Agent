
def test_roundtrip_two_dimensional(phase_shift: int|None):
    """Test roundtrip of a 2 channel input signal with `mfft` set with different
    values for `phase_shift`

    Tests for Issue https://github.com/scipy/scipy/issues/21671
    """
    n = 21
    SFT = ShortTimeFFT.from_window('hann', fs=1, nperseg=13, noverlap=7,
                                   mfft=16, phase_shift=phase_shift)
    x = np.arange(2*n, dtype=float).reshape(2, n)
    Sx = SFT.stft(x)
    y = SFT.istft(Sx, k1=n)
    xp_assert_close(y, x, atol=2 * np.finfo(SFT.win.dtype).resolution,
                    err_msg='2-dim. roundtrip failed!')

