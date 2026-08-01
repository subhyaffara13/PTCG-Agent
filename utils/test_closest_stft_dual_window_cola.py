
def test_closest_STFT_dual_window_cola(win_name, nperseg, noverlap, scale_fac):
    """Test if `closest_STFT_dual_window` generalizes `check_COLA`.

    The parameters were taken from the `check_COLA` documentation.
    Note that `check_COLA` only guarantees the existence of a dual window with constant
    values but not that those values are unity (which is clear, when investigating the
    'boxcar' examples). The values for `scale_fac` were determined empirically.
    """
    desired_dual = get_window(win_name, nperseg, fftbins=True)
    assert check_COLA(desired_dual, nperseg, noverlap), "COLA cond. violated!"

    win = np.ones(nperseg)  # check scaled window:
    d_s, s = closest_STFT_dual_window(win, nperseg-noverlap, desired_dual, scaled=True)

    res = np.finfo(desired_dual.dtype).resolution
    rel_tol_d = max(abs(d_s))*res*3
    xp_assert_close(s, scale_fac, atol=res*10,
                    err_msg=f"Scale factor off by {s/scale_fac}")
    xp_assert_close(d_s, desired_dual*scale_fac, atol=res*10, rtol=rel_tol_d,
                    err_msg="Calculated incorrect scaled window!")

    # check unscaled window:
    d_u, u = closest_STFT_dual_window(win * scale_fac, nperseg - noverlap,
                                      desired_dual, scaled=False)

    # this should be hard-coded not computed, so no need for allclose
    assert u == 1., "Scaling factor not 1 for parameter `scaled=True`!"
    xp_assert_close(d_u, desired_dual, atol=res*10, rtol=rel_tol_d,
                    err_msg="Calculated incorrect unscaled window!")

