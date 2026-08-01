
def test_map_na_exclusion(engine):  # noqa: F811
    s = Series([1.5, np.nan, 3, np.nan, 5])

    result = s.map(lambda x: x * 2, na_action="ignore", engine=engine)
    exp = s * 2
    tm.assert_series_equal(result, exp)

