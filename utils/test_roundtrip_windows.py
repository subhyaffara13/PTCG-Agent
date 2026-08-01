
def test_roundtrip_windows(window, n: int, nperseg: int, noverlap: int):
    """Roundtrip test adapted from `test_spectral.TestSTFT`.

    The parameters are taken from the methods test_roundtrip_real(),
    test_roundtrip_nola_not_cola(), test_roundtrip_float32(),
    test_roundtrip_complex().
    """
    np.random.seed(2394655)

    w = get_window(window, nperseg)
    SFT = ShortTimeFFT(w, nperseg - noverlap, fs=1, fft_mode='twosided',
                       phase_shift=None)

    z = 10 * np.random.randn(n) + 10j * np.random.randn(n)
    Sz = SFT.stft(z)
    z1 = SFT.istft(Sz, k1=len(z))
    xp_assert_close(z, z1, err_msg="Roundtrip for complex values failed")

    x = 10 * np.random.randn(n)
    Sx = SFT.stft(x)
    x1 = SFT.istft(Sx, k1=len(z))
    xp_assert_close(x.astype(np.complex128), x1,
                    err_msg="Roundtrip for float values failed")

    x32 = x.astype(np.float32)
    Sx32 = SFT.stft(x32)
    x32_1 = SFT.istft(Sx32, k1=len(x32))
    x32_1_r = x32_1.real
    xp_assert_close(x32, x32_1_r.astype(np.float32),
                    err_msg="Roundtrip for 32 Bit float values failed")
    xp_assert_close(x32.imag, np.zeros_like(x32.imag),
                    err_msg="Roundtrip for 32 Bit float values failed")

