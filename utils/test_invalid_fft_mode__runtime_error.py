
def test_invalid_fft_mode_RuntimeError():
    """Ensure exception gets raised when property `fft_mode` is invalid. """
    SFT = ShortTimeFFT(np.ones(8), hop=4, fs=1)
    # noinspection PyTypeChecker
    SFT._fft_mode = 'invalid_typ'

    with pytest.raises(RuntimeError):
        _ = SFT.f
    with pytest.raises(RuntimeError):
        SFT._fft_func(np.ones(8))
    with pytest.raises(RuntimeError):
        SFT._ifft_func(np.ones(8))

