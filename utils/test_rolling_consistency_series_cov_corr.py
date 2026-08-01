
def test_rolling_consistency_series_cov_corr(
    series_data, rolling_consistency_cases, center, ddof
):
    window, min_periods = rolling_consistency_cases

    var_x_plus_y = (
        (series_data + series_data)
        .rolling(window=window, min_periods=min_periods, center=center)
        .var(ddof=ddof)
    )
    var_x = series_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).var(ddof=ddof)
    var_y = series_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).var(ddof=ddof)
    cov_x_y = series_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).cov(series_data, ddof=ddof)
    # check that cov(x, y) == (var(x+y) - var(x) -
    # var(y)) / 2
    tm.assert_equal(cov_x_y, 0.5 * (var_x_plus_y - var_x - var_y))

    # check that corr(x, y) == cov(x, y) / (std(x) *
    # std(y))
    corr_x_y = series_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).corr(series_data)
    std_x = series_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).std(ddof=ddof)
    std_y = series_data.rolling(
        window=window, min_periods=min_periods, center=center
    ).std(ddof=ddof)
    tm.assert_equal(corr_x_y, cov_x_y / (std_x * std_y))

    if ddof == 0:
        # check that biased cov(x, y) == mean(x*y) -
        # mean(x)*mean(y)
        mean_x = series_data.rolling(
            window=window, min_periods=min_periods, center=center
        ).mean()
        mean_y = series_data.rolling(
            window=window, min_periods=min_periods, center=center
        ).mean()
        mean_x_times_y = (
            (series_data * series_data)
            .rolling(window=window, min_periods=min_periods, center=center)
            .mean()
        )
        tm.assert_equal(cov_x_y, mean_x_times_y - (mean_x * mean_y))

