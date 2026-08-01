
def test_count_arrow_string_array(any_string_dtype):
    # GH#54751
    pytest.importorskip("pyarrow")
    df = DataFrame(
        {"a": [1, 2, 3], "b": Series(["a", "b", "a"], dtype=any_string_dtype)}
    )
    result = df.groupby("a").count()
    expected = DataFrame({"b": 1}, index=Index([1, 2, 3], name="a"))
    tm.assert_frame_equal(result, expected)

