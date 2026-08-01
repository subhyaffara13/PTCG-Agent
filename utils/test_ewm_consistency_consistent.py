
def test_ewm_consistency_consistent(consistent_data, adjust, ignore_na, min_periods):
    com = 3.0

    count_x = consistent_data.expanding().count()
    mean_x = consistent_data.ewm(
        com=com, min_periods=min_periods, adjust=adjust, ignore_na=ignore_na
    ).mean()
    # check that correlation of a series with itself is either 1 or NaN
    corr_x_x = consistent_data.ewm(
        com=com, min_periods=min_periods, adjust=adjust, ignore_na=ignore_na
    ).corr(consistent_data)
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

