
def test_strip_promoter():
    arg = ["Hello!!!!", "Hello??!!"]
    strip_char = "!"
    answer = ["Hello", "Hello??"]
    for dtypes in [("T", "U"), ("U", "T")]:
        result = np.strings.strip(
            np.array(arg, dtype=dtypes[0]),
            np.array(strip_char, dtype=dtypes[1])
        )
        assert_array_equal(result, answer)
        assert result.dtype.char == "T"

