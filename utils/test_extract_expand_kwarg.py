
def test_extract_expand_kwarg(any_string_dtype):
    s = Series(["fooBAD__barBAD", np.nan, "foo"], dtype=any_string_dtype)
    expected = DataFrame(["BAD__", np.nan, np.nan], dtype=any_string_dtype)

    result = s.str.extract(".*(BAD[_]+).*")
    tm.assert_frame_equal(result, expected)

    result = s.str.extract(".*(BAD[_]+).*", expand=True)
    tm.assert_frame_equal(result, expected)

    expected = DataFrame(
        [["BAD__", "BAD"], [np.nan, np.nan], [np.nan, np.nan]], dtype=any_string_dtype
    )
    result = s.str.extract(".*(BAD[_]+).*(BAD)", expand=False)
    tm.assert_frame_equal(result, expected)

