
def test_shifts_accuracy():
    rng = np.random.default_rng(0)
    n, k = 70, 10
    A = rng.random((n, n)).astype(np.float64)
    u1, s1, vt1, _ = _svdp(A, k, shifts=None, which='SM', irl_mode=True, rng=rng)
    u2, s2, vt2, _ = _svdp(A, k, shifts=32, which='SM', irl_mode=True, rng=rng)
    # shifts <= 32 doesn't agree with shifts > 32
    # Does agree when which='LM' instead of 'SM'
    assert_allclose(s1, s2)

