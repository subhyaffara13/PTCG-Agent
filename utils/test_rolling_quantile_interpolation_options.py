
def test_rolling_quantile_interpolation_options(quantile, interpolation, data):
    # Tests that rolling window's quantile behavior is analogous to
    # Series' quantile for each interpolation option
    s = Series(data)

    q1 = s.quantile(quantile, interpolation)
    q2 = s.expanding(min_periods=1).quantile(quantile, interpolation).iloc[-1]

    if np.isnan(q1):
        assert np.isnan(q2)
    elif not IS64:
        # Less precision on 32-bit
        assert np.allclose([q1], [q2], rtol=1e-07, atol=0)
    else:
        assert q1 == q2

