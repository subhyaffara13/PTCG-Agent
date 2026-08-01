
def check_czt(x):
    # Check that czt is the equivalent of normal fft
    y = fft(x)
    y1 = czt(x)
    xp_assert_close(y1, y, rtol=1e-13)

    # Check that interpolated czt is the equivalent of normal fft
    y = fft(x, 100*len(x))
    y1 = czt(x, 100*len(x))
    xp_assert_close(y1, y, rtol=1e-12)

