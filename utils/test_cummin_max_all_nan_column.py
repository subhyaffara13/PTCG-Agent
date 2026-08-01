
def test_cummin_max_all_nan_column(method, dtype):
    item = np.nan if dtype == "float" else pd.NA
    base_df = DataFrame({"A": [1, 1, 1, 1, 2, 2, 2, 2], "B": [item] * 8})
    base_df["B"] = base_df["B"].astype(dtype)
    grouped = base_df.groupby("A")

    expected = DataFrame({"B": [item] * 8}, dtype=dtype)
    result = getattr(grouped, method)()
    tm.assert_frame_equal(expected, result)

    result = getattr(grouped["B"], method)().to_frame()
    tm.assert_frame_equal(expected, result)

