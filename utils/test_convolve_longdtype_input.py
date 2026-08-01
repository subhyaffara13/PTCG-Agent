
def test_convolve_longdtype_input(dtype, xp):
    x = np.random.random((27, 27)).astype(dtype)
    y = np.random.random((4, 4)).astype(dtype)
    if np.iscomplexobj(dtype()):
        x += .1j
        y -= .1j

    res = fftconvolve(x, y)
    xp_assert_close(res, convolve(x, y, method='direct'))
    assert res.dtype == dtype

