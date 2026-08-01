
def test_group_diff_real_frame(any_real_numpy_dtype):
    df = DataFrame(
        {
            "a": [1, 2, 3, 3, 2],
            "b": [1, 2, 3, 4, 5],
            "c": [1, 2, 3, 4, 6],
        },
        dtype=any_real_numpy_dtype,
    )
    result = df.groupby("a").diff()
    exp_dtype = "float"
    if any_real_numpy_dtype in ["int8", "int16", "float32"]:
        exp_dtype = "float32"
    expected = DataFrame(
        {
            "b": [np.nan, np.nan, np.nan, 1.0, 3.0],
            "c": [np.nan, np.nan, np.nan, 1.0, 4.0],
        },
        dtype=exp_dtype,
    )
    tm.assert_frame_equal(result, expected)

