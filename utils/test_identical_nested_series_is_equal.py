
def test_identical_nested_series_is_equal():
    # GH#22400
    x = Series(
        [
            0,
            0.0131142231938,
            1.77774652865e-05,
            np.array([0.4722720840328748, 0.4216929783681722]),
        ]
    )
    y = Series(
        [
            0,
            0.0131142231938,
            1.77774652865e-05,
            np.array([0.4722720840328748, 0.4216929783681722]),
        ]
    )
    # These two arrays should be equal, nesting could cause issue

    tm.assert_series_equal(x, x)
    tm.assert_series_equal(x, x, check_exact=True)
    tm.assert_series_equal(x, y)
    tm.assert_series_equal(x, y, check_exact=True)

