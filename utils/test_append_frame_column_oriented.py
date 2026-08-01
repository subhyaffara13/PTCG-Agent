
def test_append_frame_column_oriented(temp_hdfstore, request):
    # column oriented
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    df.index = df.index._with_freq(None)  # freq doesn't round-trip

    temp_hdfstore.append("df1", df.iloc[:, :2], axes=["columns"])
    temp_hdfstore.append("df1", df.iloc[:, 2:])
    tm.assert_frame_equal(temp_hdfstore["df1"], df)

    result = temp_hdfstore.select("df1", "columns=A")
    expected = df.reindex(columns=["A"])
    tm.assert_frame_equal(expected, result)

    # selection on the non-indexable
    request.applymarker(
        pytest.mark.xfail(
            PY312,
            reason="AST change in PY312",
            raises=ValueError,
        )
    )
    result = temp_hdfstore.select("df1", ("columns=A", "index=df.index[0:4]"))
    expected = df.reindex(columns=["A"], index=df.index[0:4])
    tm.assert_frame_equal(expected, result)

    # this isn't supported
    msg = re.escape(
        "passing a filterable condition to a non-table indexer "
        "[Filter: Not Initialized]"
    )
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.select("df1", "columns=A and index>df.index[4]")

