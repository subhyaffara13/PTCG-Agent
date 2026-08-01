
def test_moments_consistency_var_constant(
    consistent_data, adjust, ignore_na, min_periods, bias
):
    com = 3.0
    count_x = consistent_data.expanding(min_periods=min_periods).count()
    var_x = consistent_data.ewm(
        com=com, min_periods=min_periods, adjust=adjust, ignore_na=ignore_na
    ).var(bias=bias)

    # check that variance of constant series is identically 0
    assert not (var_x > 0).any(axis=None)
    expected = consistent_data * np.nan
    expected[count_x >= max(min_periods, 1)] = 0.0
    if not bias:
        expected[count_x < 2] = np.nan
    tm.assert_equal(var_x, expected)


def test_moments_consistency_var_constant(consistent_data, min_periods, ddof):
    count_x = consistent_data.expanding(min_periods=min_periods).count()
    var_x = consistent_data.expanding(min_periods=min_periods).var(ddof=ddof)

    # check that variance of constant series is identically 0
    assert not (var_x > 0).any(axis=None)
    expected = consistent_data * np.nan
    expected[count_x >= max(min_periods, 1)] = 0.0
    if ddof == 1:
        expected[count_x < 2] = np.nan
    tm.assert_equal(var_x, expected)


def test_moments_consistency_var_constant(
    consistent_data, rolling_consistency_cases, center, ddof
):
    window, min_periods = rolling_consistency_cases

    count_x = consistent_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).count()
    var_x = consistent_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).var(ddof=ddof)

    # check that variance of constant series is identically 0
    assert not (var_x > 0).any(axis=None)
    expected = consistent_data * np.nan
    expected[count_x >= max(min_periods, 1)] = 0.0
    if ddof == 1:
        expected[count_x < 2] = np.nan
    tm.assert_equal(var_x, expected)

