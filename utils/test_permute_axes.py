
def test_permute_axes():
    """Verify correctness of four-dimensional signal by permuting its
    shape. """
    n = 25
    SFT = ShortTimeFFT(np.ones(8)/8, hop=3, fs=n)
    x0 = np.arange(n, dtype=np.float64)
    Sx0 = SFT.stft(x0)
    Sx0 = Sx0.reshape((Sx0.shape[0], 1, 1, 1, Sx0.shape[-1]))
    SxT = np.moveaxis(Sx0, (0, -1), (-1, 0))

    atol = 2 * np.finfo(SFT.win.dtype).resolution
    for i in range(4):
        y = np.reshape(x0, np.roll((n, 1, 1, 1), i))
        Sy = SFT.stft(y, axis=i)
        xp_assert_close(Sy, np.moveaxis(Sx0, 0, i))

        yb0 = SFT.istft(Sy, k1=n, f_axis=i)
        xp_assert_close(yb0, y, atol=atol)
        # explicit t-axis parameter (for coverage):
        yb1 = SFT.istft(Sy, k1=n, f_axis=i, t_axis=Sy.ndim-1)
        xp_assert_close(yb1, y, atol=atol)

        SyT = np.moveaxis(Sy, (i, -1), (-1, i))
        xp_assert_close(SyT, np.moveaxis(SxT, 0, i))

        ybT = SFT.istft(SyT, k1=n, t_axis=i, f_axis=-1)
        xp_assert_close(ybT, y, atol=atol)

