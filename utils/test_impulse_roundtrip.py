
def test_impulse_roundtrip(i):
    """Roundtrip for an impulse being at different positions `i`."""
    n = 19
    w, h_n = np.ones(8), 3
    x = np.zeros(n)
    x[i] = 1

    SFT = ShortTimeFFT(w, hop=h_n, fs=1, scale_to=None, phase_shift=None)
    Sx = SFT.stft(x)
    # test slicing the input signal into two parts:
    n_q = SFT.nearest_k_p(n // 2)
    Sx0 = SFT.stft(x[:n_q], padding='zeros')
    Sx1 = SFT.stft(x[n_q:], padding='zeros')
    q0_ub = SFT.upper_border_begin(n_q)[1] - SFT.p_min
    q1_le = SFT.lower_border_end[1] - SFT.p_min
    xp_assert_close(Sx0[:, :q0_ub], Sx[:, :q0_ub], err_msg=f"{i=}")
    xp_assert_close(Sx1[:, q1_le:], Sx[:, q1_le-Sx1.shape[1]:],
                    err_msg=f"{i=}")

    Sx01 = np.hstack((Sx0[:, :q0_ub],
                      Sx0[:, q0_ub:] + Sx1[:, :q1_le],
                      Sx1[:, q1_le:]))
    xp_assert_close(Sx, Sx01, atol=1e-8, err_msg=f"{i=}")

    y = SFT.istft(Sx, 0, n)
    xp_assert_close(y, x, atol=1e-8, err_msg=f"{i=}")
    y0 = SFT.istft(Sx, 0, n//2)
    xp_assert_close(x[:n//2], y0, atol=1e-8, err_msg=f"{i=}")
    y1 = SFT.istft(Sx, n // 2, n)
    xp_assert_close(x[n // 2:], y1, atol=1e-8, err_msg=f"{i=}")

