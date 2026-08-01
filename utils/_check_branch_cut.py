
def _check_branch_cut(f, x0, dx, re_sign=1, im_sign=-1, sig_zero_ok=False,
                      dtype=complex):
    """
    Check for a branch cut in a function.

    Assert that `x0` lies on a branch cut of function `f` and `f` is
    continuous from the direction `dx`.

    Parameters
    ----------
    f : func
        Function to check
    x0 : array-like
        Point on branch cut
    dx : array-like
        Direction to check continuity in
    re_sign, im_sign : {1, -1}
        Change of sign of the real or imaginary part expected
    sig_zero_ok : bool
        Whether to check if the branch cut respects signed zero (if applicable)
    dtype : dtype
        Dtype to check (should be complex)

    """
    x0 = np.atleast_1d(x0).astype(dtype)
    dx = np.atleast_1d(dx).astype(dtype)

    if np.dtype(dtype).char == 'F':
        scale = np.finfo(dtype).eps * 1e2
        atol = np.float32(1e-2)
    else:
        scale = np.finfo(dtype).eps * 1e3
        atol = 1e-4

    y0 = f(x0)
    yp = f(x0 + dx * scale * np.absolute(x0) / np.absolute(dx))
    ym = f(x0 - dx * scale * np.absolute(x0) / np.absolute(dx))

    assert_(np.all(np.absolute(y0.real - yp.real) < atol), (y0, yp))
    assert_(np.all(np.absolute(y0.imag - yp.imag) < atol), (y0, yp))
    assert_(np.all(np.absolute(y0.real - ym.real * re_sign) < atol), (y0, ym))
    assert_(np.all(np.absolute(y0.imag - ym.imag * im_sign) < atol), (y0, ym))

    if sig_zero_ok:
        # check that signed zeros also work as a displacement
        jr = (x0.real == 0) & (dx.real != 0)
        ji = (x0.imag == 0) & (dx.imag != 0)
        if np.any(jr):
            x = x0[jr]
            x.real = ncu.NZERO
            ym = f(x)
            assert_(
                np.all(np.absolute(y0[jr].real - ym.real * re_sign) < atol),
                (y0[jr], ym),
            )
            assert_(
                np.all(np.absolute(y0[jr].imag - ym.imag * im_sign) < atol),
                (y0[jr], ym),
            )

        if np.any(ji):
            x = x0[ji]
            x.imag = ncu.NZERO
            ym = f(x)
            assert_(
                np.all(np.absolute(y0[ji].real - ym.real * re_sign) < atol),
                (y0[ji], ym),
            )
            assert_(
                np.all(np.absolute(y0[ji].imag - ym.imag * im_sign) < atol),
                (y0[ji], ym),
            )

