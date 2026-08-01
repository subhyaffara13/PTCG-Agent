
def test_partition_with_name(any_string_dtype):
    # GH 12617

    s = Series(["a,b", "c,d"], name="xxx", dtype=any_string_dtype)
    result = s.str.partition(",")
    expected = DataFrame(
        {0: ["a", "c"], 1: [",", ","], 2: ["b", "d"]}, dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

