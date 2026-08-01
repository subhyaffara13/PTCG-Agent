
def test_skip_group_keys():
    tsf = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )

    grouped = tsf.groupby(lambda x: x.month, group_keys=False)
    result = grouped.apply(lambda x: x.sort_values(by="A")[:3])

    pieces = [group.sort_values(by="A")[:3] for key, group in grouped]

    expected = pd.concat(pieces)
    tm.assert_frame_equal(result, expected)

    grouped = tsf["A"].groupby(lambda x: x.month, group_keys=False)
    result = grouped.apply(lambda x: x.sort_values()[:3])

    pieces = [group.sort_values()[:3] for key, group in grouped]

    expected = pd.concat(pieces)
    tm.assert_series_equal(result, expected)

