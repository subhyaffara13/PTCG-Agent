
def test_put(temp_hdfstore):
    store = temp_hdfstore
    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    df = DataFrame(
        np.random.default_rng(2).standard_normal((20, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=20, freq="B"),
    )
    store["a"] = ts
    store["b"] = df[:10]
    store["foo/bar/bah"] = df[:10]
    store["foo"] = df[:10]
    store["/foo"] = df[:10]
    store.put("c", df[:10], format="table")

    # not OK, not a table
    msg = "Can only append to Tables"
    with pytest.raises(ValueError, match=msg):
        store.put("b", df[10:], append=True)

    # node does not currently exist, test _is_table_type returns False
    # in this case
    with pytest.raises(ValueError, match=msg):
        store.put("f", df[10:], append=True)

    # can't put to a table (use append instead)
    with pytest.raises(ValueError, match=msg):
        store.put("c", df[10:], append=True)

    # overwrite table
    store.put("c", df[:10], format="table", append=False)
    tm.assert_frame_equal(df[:10], store["c"])

