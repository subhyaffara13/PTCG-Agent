
def test_groupby_count_return_arrow_dtype(data_missing):
    df = pd.DataFrame({"A": [1, 1], "B": data_missing, "C": data_missing})
    result = df.groupby("A").count()
    expected = pd.DataFrame(
        [[1, 1]],
        index=pd.Index([1], name="A"),
        columns=["B", "C"],
        dtype="int64[pyarrow]",
    )
    tm.assert_frame_equal(result, expected)

