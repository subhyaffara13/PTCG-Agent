
def test_append_series(temp_hdfstore):
    # basic
    ss = Series(range(20), dtype=np.float64, index=[f"i_{i}" for i in range(20)])
    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    ns = Series(np.arange(100))

    temp_hdfstore.append("ss", ss)
    result = temp_hdfstore["ss"]
    tm.assert_series_equal(result, ss)
    assert result.name is None

    temp_hdfstore.append("ts", ts)
    result = temp_hdfstore["ts"]
    tm.assert_series_equal(result, ts)
    assert result.name is None

    ns.name = "foo"
    temp_hdfstore.append("ns", ns)
    result = temp_hdfstore["ns"]
    tm.assert_series_equal(result, ns)
    assert result.name == ns.name

    # select on the values
    expected = ns[ns > 60]
    result = temp_hdfstore.select("ns", "foo>60")
    tm.assert_series_equal(result, expected)

    # select on the index and values
    expected = ns[(ns > 70) & (ns.index < 90)]
    # Reading/writing RangeIndex info is not supported yet
    expected.index = Index(expected.index._data)
    result = temp_hdfstore.select("ns", "foo>70 and index<90")
    tm.assert_series_equal(result, expected, check_index_type=True)

    # multi-index
    mi = DataFrame(np.random.default_rng(2).standard_normal((5, 1)), columns=["A"])
    mi["B"] = np.arange(len(mi))
    mi["C"] = "foo"
    mi.loc[3:5, "C"] = "bar"
    mi.set_index(["C", "B"], inplace=True)
    s = mi.stack()
    s.index = s.index.droplevel(2)
    temp_hdfstore.append("mi", s)
    tm.assert_series_equal(temp_hdfstore["mi"], s, check_index_type=True)

