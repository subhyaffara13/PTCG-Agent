
def test_reindex_multiindex_automatic_level(name, expected_match_level_a):
    series = Series([26.73, 24.255], index=Index([81, 82], name=name))
    target = MultiIndex.from_product(
        [[81, 82], [np.nan], ["2018-06-01", "2018-07-01"]], names=["a", "b", "c"]
    )

    result = series.reindex(target)

    if expected_match_level_a:
        expected = Series(
            data=[26.73, 26.73, 24.255, 24.255],
            index=MultiIndex.from_product(
                [[81, 82], [np.nan], ["2018-06-01", "2018-07-01"]],
                names=["a", "b", "c"],
            ),
            dtype=series.dtype,
        )
    else:
        expected = Series(
            data=[np.nan] * 4,
            index=MultiIndex.from_product(
                [[81, 82], [np.nan], ["2018-06-01", "2018-07-01"]],
                names=["a", "b", "c"],
            ),
            dtype=series.dtype,
        )

    tm.assert_series_equal(result, expected)

