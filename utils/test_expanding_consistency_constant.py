
def test_expanding_consistency_constant(consistent_data, min_periods):
    count_x = consistent_data.expanding().count()
    mean_x = consistent_data.expanding(min_periods=min_periods).mean()
    # check that correlation of a series with itself is either 1 or NaN
    corr_x_x = consistent_data.expanding(min_periods=min_periods).corr(consistent_data)

    exp = (
        consistent_data.max()
        if isinstance(consistent_data, Series)
        else consistent_data.max().max()
    )

    # check mean of constant series
    expected = consistent_data * np.nan
    expected[count_x >= max(min_periods, 1)] = exp
    tm.assert_equal(mean_x, expected)

    # check correlation of constant series with itself is NaN
    expected[:] = np.nan
    tm.assert_equal(corr_x_x, expected)

