
def test_extent(n, m, fft_mode: FFT_MODE_TYPE):
    """Ensure that the `extent()` method is correct. """
    SFT = ShortTimeFFT(np.ones(m), hop=m, fs=m, fft_mode=fft_mode)

    t0 = SFT.t(n)[0]  # first timestamp
    t1 = SFT.t(n)[-1] + SFT.delta_t  # last timestamp + 1
    t0c, t1c = t0 - SFT.delta_t / 2, t1 - SFT.delta_t / 2  # centered timestamps

    f0 = SFT.f[0]  # first frequency
    f1 = SFT.f[-1] + SFT.delta_f  # last frequency + 1
    f0c, f1c = f0 - SFT.delta_f / 2, f1 - SFT.delta_f / 2  # centered frequencies

    assert SFT.extent(n, 'tf', False) == (t0, t1, f0, f1)
    assert SFT.extent(n, 'ft', False) == (f0, f1, t0, t1)
    assert SFT.extent(n, 'tf', True) == (t0c, t1c, f0c, f1c)
    assert SFT.extent(n, 'ft', True) == (f0c, f1c, t0c, t1c)

