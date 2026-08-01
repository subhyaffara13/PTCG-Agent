
def test_moments_consistency_var(all_data, adjust, ignore_na, min_periods, bias):
    com = 3.0

    mean_x = all_data.ewm(
        com=com, min_periods=min_periods, adjust=adjust, ignore_na=ignore_na
    ).mean()
    var_x = all_data.ewm(
        com=com, min_periods=min_periods, adjust=adjust, ignore_na=ignore_na
    ).var(bias=bias)
    assert not (var_x < 0).any(axis=None)

    if bias:
        # check that biased var(x) == mean(x^2) - mean(x)^2
        mean_x2 = (
            (all_data * all_data)
            .ewm(com=com, min_periods=min_periods, adjust=adjust, ignore_na=ignore_na)
            .mean()
        )
        tm.assert_equal(var_x, mean_x2 - (mean_x * mean_x))


def test_moments_consistency_var(all_data, min_periods, ddof):
    var_x = all_data.expanding(min_periods=min_periods).var(ddof=ddof)
    assert not (var_x < 0).any(axis=None)

    if ddof == 0:
        # check that biased var(x) == mean(x^2) - mean(x)^2
        mean_x2 = (all_data * all_data).expanding(min_periods=min_periods).mean()
        mean_x = all_data.expanding(min_periods=min_periods).mean()
        tm.assert_equal(var_x, mean_x2 - (mean_x * mean_x))


def test_moments_consistency_var(all_data, rolling_consistency_cases, center, ddof):
    window, min_periods = rolling_consistency_cases

    var_x = all_data.rolling(window=window, min_periods=min_periods, center=center).var(
        ddof=ddof
    )
    assert not (var_x < 0).any(axis=None)

    if ddof == 0:
        # check that biased var(x) == mean(x^2) - mean(x)^2
        mean_x = all_data.rolling(
            window=window, min_periods=min_periods, center=center
        ).mean()
        mean_x2 = (
            (all_data * all_data)
            .rolling(window=window, min_periods=min_periods, center=center)
            .mean()
        )
        tm.assert_equal(var_x, mean_x2 - (mean_x * mean_x))

