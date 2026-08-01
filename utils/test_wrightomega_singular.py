
def test_wrightomega_singular():
    pts = [complex(-1.0, np.pi),
           complex(-1.0, -np.pi)]
    for p in pts:
        res = sc.wrightomega(p)
        assert_equal(res, -1.0)
        assert_(np.signbit(res.imag) == np.bool_(False))

