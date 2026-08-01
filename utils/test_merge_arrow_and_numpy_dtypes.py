
def test_merge_arrow_and_numpy_dtypes(dtype):
    # GH#52406
    pytest.importorskip("pyarrow")
    df = DataFrame({"a": [1, 2]}, dtype=dtype)
    df2 = DataFrame({"a": [1, 2]}, dtype="int64[pyarrow]")
    result = df.merge(df2)
    expected = df.copy()
    tm.assert_frame_equal(result, expected)

    result = df2.merge(df)
    expected = df2.copy()
    tm.assert_frame_equal(result, expected)

