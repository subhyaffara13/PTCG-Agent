
def test_compare_ea_and_np_dtype(val1, val2):
    # GH 48966
    arr = [4.0, val1]
    ser = pd.Series([1, val2], dtype="Int64")

    df1 = pd.DataFrame({"a": arr, "b": [1.0, 2]})
    df2 = pd.DataFrame({"a": ser, "b": [1.0, 2]})
    expected = pd.DataFrame(
        {
            ("a", "self"): arr,
            ("a", "other"): ser,
            ("b", "self"): np.nan,
            ("b", "other"): np.nan,
        }
    )
    if val1 is pd.NA and val2 is pd.NA:
        # GH#18463 TODO: is this really the desired behavior?
        expected.loc[1, ("a", "self")] = np.nan

    if val1 is pd.NA:
        # can't compare with numpy array if it contains pd.NA
        with pytest.raises(TypeError, match="boolean value of NA is ambiguous"):
            result = df1.compare(df2, keep_shape=True)
    else:
        result = df1.compare(df2, keep_shape=True)
        tm.assert_frame_equal(result, expected)

