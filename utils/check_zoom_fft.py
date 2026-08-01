
def check_zoom_fft(x):
    # Check that zoom_fft is the equivalent of normal fft
    y = fft(x)
    y1 = zoom_fft(x, [0, 2-2./len(y)], endpoint=True)
    xp_assert_close(y1, y, rtol=1e-11, atol=1e-14)
    y1 = zoom_fft(x, [0, 2])
    xp_assert_close(y1, y, rtol=1e-11, atol=1e-14)

    # Test fn scalar
    y1 = zoom_fft(x, 2-2./len(y), endpoint=True)
    xp_assert_close(y1, y, rtol=1e-11, atol=1e-14)
    y1 = zoom_fft(x, 2)
    xp_assert_close(y1, y, rtol=1e-11, atol=1e-14)

    # Check that zoom_fft with oversampling is equivalent to zero padding
    over = 10
    yover = fft(x, over*len(x))
    y2 = zoom_fft(x, [0, 2-2./len(yover)], m=len(yover), endpoint=True)
    xp_assert_close(y2, yover, rtol=1e-12, atol=1e-10)
    y2 = zoom_fft(x, [0, 2], m=len(yover))
    xp_assert_close(y2, yover, rtol=1e-12, atol=1e-10)

    # Check that zoom_fft works on a subrange
    w = np.linspace(0, 2-2./len(x), len(x))
    f1, f2 = w[3], w[6]
    y3 = zoom_fft(x, [f1, f2], m=3*over+1, endpoint=True)
    idx3 = slice(3*over, 6*over+1)
    xp_assert_close(y3, yover[idx3], rtol=1e-13)

