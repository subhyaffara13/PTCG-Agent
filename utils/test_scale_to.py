
def test_scale_to():
    """Verify `scale_to()` method."""
    SFT = ShortTimeFFT(np.ones(4) * 2, hop=4, fs=1, scale_to=None)

    SFT.scale_to('magnitude')
    assert SFT.scaling == 'magnitude'
    assert SFT.fac_psd == 2.0
    assert SFT.fac_magnitude == 1

    SFT.scale_to('psd')
    assert SFT.scaling == 'psd'
    assert SFT.fac_psd == 1
    assert SFT.fac_magnitude == 0.5

    SFT.scale_to('psd')  # needed for coverage

    for scale, s_fac in zip(('magnitude', 'psd'), (8, 4)):
        SFT = ShortTimeFFT(np.ones(4) * 2, hop=4, fs=1, scale_to=None)
        dual_win = SFT.dual_win.copy()

        SFT.scale_to(cast(Literal['magnitude', 'psd'], scale))
        xp_assert_close(SFT.dual_win, dual_win * s_fac)

