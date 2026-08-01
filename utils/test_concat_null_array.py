
def test_concat_null_array():
    df = pd.DataFrame({"a": [None, None]}, dtype=ArrowDtype(pa.null()))
    df2 = pd.DataFrame({"a": [0, 1]}, dtype="int64[pyarrow]")

    result = pd.concat([df, df2], ignore_index=True)
    expected = pd.DataFrame({"a": [None, None, 0, 1]}, dtype="int64[pyarrow]")
    tm.assert_frame_equal(result, expected)

