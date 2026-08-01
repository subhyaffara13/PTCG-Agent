
def test_object_dtype_preserved():
    # https://github.com/pandas-dev/pandas/pull/60694
    # When the input has object dtype, the result should as
    # well even when infer_string is True.
    df = DataFrame(
        {
            "x": [1, 0, 0],
            "y": [0, 1, 0],
        },
    )
    df.columns = df.columns.astype("object")
    result = from_dummies(df, default_category="z")
    expected = DataFrame({"": ["x", "y", "z"]}, dtype="object")
    tm.assert_frame_equal(result, expected)

