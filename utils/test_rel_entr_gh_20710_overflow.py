
def test_rel_entr_gh_20710_overflow():
    special.seterr(all='ignore')
    inputs = np.array([
        # x, y
        # Overflow
        (4, 2.22e-308),
        # Underflow
        (1e-200, 1e+200),
        # Subnormal
        (2.22e-308, 1e15),
    ])
    # Known values produced using `x * mpmath.log(x / y)` with dps=30
    expected = [
        2839.139983229607,
        -9.210340371976183e-198,
        -1.6493212008074475e-305,
    ]
    x = inputs[:, 0]
    y = inputs[:, 1]
    assert_allclose(special.rel_entr(x, y), expected, rtol=1e-13, atol=0)

