
def test_merge_pyarrow_datetime_duplicates():
    # GH#61926
    pytest.importorskip("pyarrow")

    t = pd.date_range("2025-07-06", periods=3, freq="h")
    df1 = DataFrame({"time": t, "val1": [1, 2, 3]})
    df1 = df1.convert_dtypes(dtype_backend="pyarrow")

    df2 = DataFrame({"time": t.repeat(2), "val2": [10, 20, 30, 40, 50, 60]})
    df2 = df2.convert_dtypes(dtype_backend="pyarrow")

    result = merge(df1, df2, on="time", how="left")

    expected = DataFrame(
        {
            "time": t.repeat(2),
            "val1": [1, 1, 2, 2, 3, 3],
            "val2": [10, 20, 30, 40, 50, 60],
        }
    )
    expected = expected.convert_dtypes(dtype_backend="pyarrow")
    tm.assert_frame_equal(result, expected)

