
def test_cummin_nan_in_some_values(dtypes_for_minmax):
    # Explicit cast to float to avoid implicit cast when setting nan
    base_df = DataFrame({"A": [1, 1, 1, 1, 2, 2, 2, 2], "B": [3, 4, 3, 2, 2, 3, 2, 1]})
    base_df = base_df.astype({"B": "float"})
    base_df.loc[[0, 2, 4, 6], "B"] = np.nan
    expected = DataFrame({"B": [np.nan, 4, np.nan, 2, np.nan, 3, np.nan, 1]})
    result = base_df.groupby("A").cummin()
    tm.assert_frame_equal(result, expected)
    expected = (
        base_df.groupby("A", group_keys=False).B.apply(lambda x: x.cummin()).to_frame()
    )
    tm.assert_frame_equal(result, expected)

