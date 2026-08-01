
def test_idxmin_idxmax_transform_args(how, skipna, numeric_only):
    # GH#55268 - ensure *args are passed through when calling transform
    df = DataFrame({"a": [1, 1, 1, 2], "b": [3.0, 4.0, np.nan, 6.0], "c": list("abcd")})
    gb = df.groupby("a")
    if skipna:
        result = gb.transform(how, skipna, numeric_only)
        expected = gb.transform(how, skipna=skipna, numeric_only=numeric_only)
        tm.assert_frame_equal(result, expected)
    else:
        msg = f"{how} with skipna=False encountered an NA value"
        with pytest.raises(ValueError, match=msg):
            gb.transform(how, skipna, numeric_only)

