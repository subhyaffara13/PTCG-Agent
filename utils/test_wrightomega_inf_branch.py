
def test_wrightomega_inf_branch():
    pts = [complex(-np.inf, np.pi/4),
           complex(-np.inf, -np.pi/4),
           complex(-np.inf, 3*np.pi/4),
           complex(-np.inf, -3*np.pi/4)]
    expected_results = [complex(0.0, 0.0),
                        complex(0.0, -0.0),
                        complex(-0.0, 0.0),
                        complex(-0.0, -0.0)]
    for p, expected in zip(pts, expected_results):
        res = sc.wrightomega(p)
        # We can't use assert_equal(res, expected) because in older versions of
        # numpy, assert_equal doesn't check the sign of the real and imaginary
        # parts when comparing complex zeros. It does check the sign when the
        # arguments are *real* scalars.
        assert_equal(res.real, expected.real)
        assert_equal(res.imag, expected.imag)

