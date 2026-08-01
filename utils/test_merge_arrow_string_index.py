
def test_merge_arrow_string_index(any_string_dtype):
    # GH#54894
    pytest.importorskip("pyarrow")
    left = DataFrame({"a": ["a", "b"]}, dtype=any_string_dtype)
    right = DataFrame({"b": 1}, index=Index(["a", "c"], dtype=any_string_dtype))
    result = left.merge(right, left_on="a", right_index=True, how="left")
    expected = DataFrame(
        {"a": Series(["a", "b"], dtype=any_string_dtype), "b": [1, np.nan]}
    )
    tm.assert_frame_equal(result, expected)

