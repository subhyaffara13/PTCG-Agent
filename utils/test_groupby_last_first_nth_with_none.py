
def test_groupby_last_first_nth_with_none(method, nulls_fixture):
    # GH29645
    expected = Series(["y"], dtype=object)
    data = Series(
        [nulls_fixture, nulls_fixture, nulls_fixture, "y", nulls_fixture],
        index=[0, 0, 0, 0, 0],
        dtype=object,
    ).groupby(level=0)

    if method == "nth":
        result = getattr(data, method)(3)
    else:
        result = getattr(data, method)()

    tm.assert_series_equal(result, expected)

