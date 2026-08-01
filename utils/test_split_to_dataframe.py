
def test_split_to_dataframe(any_string_dtype):
    s = Series(["some_equal_splits", "with_no_nans"], dtype=any_string_dtype)
    result = s.str.split("_", expand=True)
    exp = DataFrame(
        {0: ["some", "with"], 1: ["equal", "no"], 2: ["splits", "nans"]},
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, exp)

