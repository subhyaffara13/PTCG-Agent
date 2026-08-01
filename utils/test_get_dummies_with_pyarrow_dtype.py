
def test_get_dummies_with_pyarrow_dtype(any_string_dtype, dtype):
    s = Series(["a|b", "a|c", np.nan], dtype=any_string_dtype)
    result = s.str.get_dummies("|", dtype=dtype)
    expected = DataFrame(
        [[1, 1, 0], [1, 0, 1], [0, 0, 0]],
        columns=list("abc"),
        dtype=dtype,
    )
    tm.assert_frame_equal(result, expected)

