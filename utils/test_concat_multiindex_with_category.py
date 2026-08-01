
def test_concat_multiindex_with_category():
    df1 = DataFrame(
        {
            "c1": Series(list("abc"), dtype="category"),
            "c2": Series(list("eee"), dtype="category"),
            "i2": Series([1, 2, 3]),
        }
    )
    df1 = df1.set_index(["c1", "c2"])
    df2 = DataFrame(
        {
            "c1": Series(list("abc"), dtype="category"),
            "c2": Series(list("eee"), dtype="category"),
            "i2": Series([4, 5, 6]),
        }
    )
    df2 = df2.set_index(["c1", "c2"])
    result = concat([df1, df2])
    expected = DataFrame(
        {
            "c1": Series(list("abcabc"), dtype="category"),
            "c2": Series(list("eeeeee"), dtype="category"),
            "i2": Series([1, 2, 3, 4, 5, 6]),
        }
    )
    expected = expected.set_index(["c1", "c2"])
    tm.assert_frame_equal(result, expected)

