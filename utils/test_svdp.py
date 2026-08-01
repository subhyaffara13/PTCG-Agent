
def test_svdp(ctor, dtype, irl, which):
    rng = np.random.default_rng(1757937293955503)
    n, m, k = 10, 20, 3
    if which == 'SM' and not irl:
        message = "`which`='SM' requires irl_mode=True"
        with assert_raises(ValueError, match=message):
            check_svdp(n, m, ctor, dtype, k, irl, which, rng=rng)
    else:
        check_svdp(n, m, ctor, dtype, k, irl, which, rng=rng)

