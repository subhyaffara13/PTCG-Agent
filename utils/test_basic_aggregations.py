
def test_basic_aggregations(dtype):
    data = Series(np.arange(9) // 3, index=np.arange(9), dtype=dtype)

    index = np.arange(9)
    np.random.default_rng(2).shuffle(index)
    data = data.reindex(index)

    grouped = data.groupby(lambda x: x // 3, group_keys=False)

    for k, v in grouped:
        assert len(v) == 3

    agged = grouped.aggregate(np.mean)
    assert agged[1] == 1

    expected = grouped.agg(np.mean)
    tm.assert_series_equal(agged, expected)  # shorthand
    tm.assert_series_equal(agged, grouped.mean())
    result = grouped.sum()
    expected = grouped.agg(np.sum)
    if dtype == "int32":
        # NumPy's sum returns int64
        expected = expected.astype("int32")
    tm.assert_series_equal(result, expected)

    expected = grouped.apply(lambda x: x * x.sum())
    transformed = grouped.transform(lambda x: x * x.sum())
    assert transformed[7] == 12
    tm.assert_series_equal(transformed, expected)

    value_grouped = data.groupby(data)
    result = value_grouped.aggregate(np.mean)
    tm.assert_series_equal(result, agged, check_index_type=False)

    # complex agg
    agged = grouped.aggregate([np.mean, np.std])

    msg = r"nested renamer is not supported"
    with pytest.raises(pd.errors.SpecificationError, match=msg):
        grouped.aggregate({"one": np.mean, "two": np.std})

    # corner cases
    msg = "Must produce aggregated value"
    # exception raised is type Exception
    with pytest.raises(Exception, match=msg):
        grouped.aggregate(lambda x: x * 2)

