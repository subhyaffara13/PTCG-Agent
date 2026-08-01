
def test_query_long_float_literal(temp_hdfstore):
    # GH 14241
    df = DataFrame({"A": [1000000000.0009, 1000000000.0011, 1000000000.0015]})

    temp_hdfstore.append("test", df, format="table", data_columns=True)

    cutoff = 1000000000.0006
    result = temp_hdfstore.select("test", f"A < {cutoff:.4f}")
    assert result.empty

    cutoff = 1000000000.0010
    result = temp_hdfstore.select("test", f"A > {cutoff:.4f}")
    expected = df.loc[[1, 2], :]
    tm.assert_frame_equal(expected, result)

    exact = 1000000000.0011
    result = temp_hdfstore.select("test", f"A == {exact:.4f}")
    expected = df.loc[[1], :]
    tm.assert_frame_equal(expected, result)

