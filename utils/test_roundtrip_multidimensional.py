
def test_roundtrip_multidimensional(fft_mode: FFT_MODE_TYPE):
    """Test roundtrip of a multidimensional input signal versus its components.

    This test can uncover potential problems with `fftshift()`.
    """
    n = 9
    x = np.arange(4*n*2, dtype=np.float64).reshape(4, n, 2)
    SFT = ShortTimeFFT(get_window('hann', 4), hop=2, fs=1,
                       scale_to='magnitude', fft_mode=fft_mode)
    Sx = SFT.stft(x, axis=1)
    y = SFT.istft(Sx, k1=n, f_axis=1, t_axis=-1)
    xp_assert_close(y, x.astype(y.dtype), err_msg='Multidim. roundtrip failed!')

    for i, j in product(range(x.shape[0]), range(x.shape[2])):
        y_ = SFT.istft(Sx[i, :, j, :], k1=n)
        xp_assert_close(y_, x[i, :, j].astype(y_.dtype),
                        err_msg="Multidim. roundtrip for component " +
                        f"x[{i}, :, {j}] and {fft_mode=} failed!")

