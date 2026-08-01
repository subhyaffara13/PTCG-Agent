
def test_closest_STFT_dual_window_roundtrip(win_name, m, hop, sym_win, scaled):
    """Do roundtrip, i.e., compare dual of dual windows.

    The  default for parameter `desired_dual` is also verified.
    """
    win = get_window(win_name, m, not sym_win)
    d1, s1 = closest_STFT_dual_window(win, hop, np.ones_like(win), scaled=scaled)
    d2, s2 = closest_STFT_dual_window(win, hop, scaled=scaled)  # equals d1, s1
    d3, s3 = closest_STFT_dual_window(d1, hop, win * s1, scaled=True)  # roundtrip

    # (d1, s1) == (d2, s2) should hold, but the BLAS backend used to calculate the inner
    # product in `closest_STFT_dual_window` does not guarantee exact reproducibility
    # due to indeterministic summation order during parallel execution. Hence, only
    # approximate equality is verified. Consult NumPy 29873 issue for discussion.
    res = np.finfo(win.dtype).resolution  # 1e-15 for float64
    err_msg = "Default for parameter `desired_dual` is not ok!"
    xp_assert_close(d2, d1, atol=res, err_msg=err_msg)
    xp_assert_close(s2, s1, atol=res, err_msg=err_msg)

    xp_assert_close(s1*s3, 1., atol=res*5, err_msg="Invalid Scale factors")
    xp_assert_close(d3, win, atol=res*5, err_msg="Roundtrip failed!")

    if scaled:  # check that scaling factor is correct:
        d3, _ = closest_STFT_dual_window(win, hop, np.ones(m) * s1, scaled=False)
        xp_assert_close(d3, d1, atol=res, err_msg="Roundtrip failed!")

