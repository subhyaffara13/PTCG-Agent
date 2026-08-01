
def test_fftpack_equivalience(func, type, norm, xp):
    x = np.random.rand(8, 16)
    fftpack_res = xp.asarray(getattr(fftpack, func.__name__)(x, type, norm=norm))
    x = xp.asarray(x)
    fft_res = getattr(fft, func.__name__)(x, type, norm=norm)

    xp_assert_close(fft_res, fftpack_res)

