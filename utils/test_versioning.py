
def test_versioning(temp_hdfstore):
    store = temp_hdfstore
    store["a"] = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    store["b"] = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    df = DataFrame(
        np.random.default_rng(2).standard_normal((20, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=20, freq="B"),
    )
    store.append("df1", df[:10])
    store.append("df1", df[10:])
    assert store.root.a._v_attrs.pandas_version == "0.15.2"
    assert store.root.b._v_attrs.pandas_version == "0.15.2"
    assert store.root.df1._v_attrs.pandas_version == "0.15.2"

    # write a file and wipe its versioning
    store.append("df2", df)

    # this is an error because its table_type is appendable, but no
    # version info
    store.get_node("df2")._v_attrs.pandas_version = None

    msg = "'NoneType' object has no attribute 'startswith'"

    with pytest.raises(Exception, match=msg):
        store.select("df2")

