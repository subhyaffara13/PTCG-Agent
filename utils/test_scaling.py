
def test_scaling(scale_to: Literal['magnitude', 'psd'], fac_psd, fac_mag):
    """Verify scaling calculations.

    * Verify passing `scale_to`parameter  to ``__init__().
    * Roundtrip while changing scaling factor.
    """
    SFT = ShortTimeFFT(np.ones(4) * 2, hop=4, fs=1, scale_to=scale_to)
    assert SFT.fac_psd == fac_psd
    assert SFT.fac_magnitude == fac_mag
    # increase coverage by accessing properties twice:
    assert SFT.fac_psd == fac_psd
    assert SFT.fac_magnitude == fac_mag

    x = np.fft.irfft([0, 0, 7, 0, 0, 0, 0])  # periodic signal
    Sx = SFT.stft(x)
    Sx_mag, Sx_psd = Sx * SFT.fac_magnitude, Sx * SFT.fac_psd

    SFT.scale_to('magnitude')
    x_mag = SFT.istft(Sx_mag, k1=len(x))
    xp_assert_close(x_mag, x)

    SFT.scale_to('psd')
    x_psd = SFT.istft(Sx_psd, k1=len(x))
    xp_assert_close(x_psd, x)

