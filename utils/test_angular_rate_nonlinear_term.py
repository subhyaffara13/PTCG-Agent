
def test_angular_rate_nonlinear_term():
    # The only simple test is to check that the term is zero when
    # the rotation vector
    np.random.seed(0)
    rv = np.random.rand(4, 3)
    assert_allclose(_angular_acceleration_nonlinear_term(rv, rv), 0,
                    atol=1e-19)

