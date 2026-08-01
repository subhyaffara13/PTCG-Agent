
def test_dual_win_roundtrip():
    """Verify the duality of `win` and `dual_win`.

    Note that this test does not work for arbitrary windows, since dual windows
    are not unique. It always works for invertible STFTs if the windows do not
    overlap.
    """
    # Non-standard values for keyword arguments (except for `scale_to`):
    kw = dict(hop=4, fs=1, fft_mode='twosided', mfft=8, scale_to=None,
              phase_shift=2)
    SFT0 = ShortTimeFFT(np.ones(4), **kw)
    SFT1 = ShortTimeFFT.from_dual(SFT0.dual_win, **kw)
    xp_assert_close(SFT1.dual_win, SFT0.win)

