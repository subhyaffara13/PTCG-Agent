
def test_coordinates_array_mask(temp_hdfstore):
    store = temp_hdfstore
    df = DataFrame(
        np.random.default_rng(2).standard_normal((1000, 2)),
        index=date_range("20000101", periods=1000),
    )
    store.append("df", df)
    c = store.select_column("df", "index")
    where = c[DatetimeIndex(c).month == 5].index
    expected = df.iloc[where]

    # locations
    result = store.select("df", where=where)
    tm.assert_frame_equal(result, expected)

    # boolean
    result = store.select("df", where=where)
    tm.assert_frame_equal(result, expected)

    # invalid
    msg = "where must be passed as a string, PyTablesExpr, or list-like of PyTablesExpr"
    with pytest.raises(TypeError, match=msg):
        store.select("df", where=np.arange(len(df), dtype="float64"))

    with pytest.raises(TypeError, match=msg):
        store.select("df", where=np.arange(len(df) + 1))

    with pytest.raises(TypeError, match=msg):
        store.select("df", where=np.arange(len(df)), start=5)

    with pytest.raises(TypeError, match=msg):
        store.select("df", where=np.arange(len(df)), start=5, stop=10)

    # selection with filter
    selection = date_range("20000101", periods=500)
    result = store.select("df", where="index in selection")
    expected = df[df.index.isin(selection)]
    tm.assert_frame_equal(result, expected)

    # list
    df = DataFrame(np.random.default_rng(2).standard_normal((10, 2)))
    store.append("df2", df)
    result = store.select("df2", where=[0, 3, 5])
    expected = df.iloc[[0, 3, 5]]
    tm.assert_frame_equal(result, expected)

    # boolean
    where = [True] * 10
    where[-2] = False
    result = store.select("df2", where=where)
    expected = df.loc[where]
    tm.assert_frame_equal(result, expected)

    # start/stop
    result = store.select("df2", start=5, stop=10)
    expected = df[5:10]
    tm.assert_frame_equal(result, expected)

