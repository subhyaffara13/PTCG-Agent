
def test_int_args():
    # Integer argument `a` was producing all 0s
    xp_assert_close(abs(czt([0, 1], m=10, a=2)), 0.5*np.ones(10), rtol=1e-15)
    xp_assert_close(czt_points(11, w=2),
                    1/(2**np.arange(11, dtype=np.complex128)), rtol=1e-30)

