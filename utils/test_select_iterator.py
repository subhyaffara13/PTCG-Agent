
def test_select_iterator(temp_hdfstore):
    # single table
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    temp_hdfstore.append("df", df)

    expected = temp_hdfstore.select("df")

    results = list(temp_hdfstore.select("df", iterator=True))
    result = concat(results)
    tm.assert_frame_equal(expected, result)

    results = list(temp_hdfstore.select("df", chunksize=2))
    assert len(results) == 5
    result = concat(results)
    tm.assert_frame_equal(expected, result)

    results = list(temp_hdfstore.select("df", chunksize=2))
    result = concat(results)
    tm.assert_frame_equal(result, expected)

