
def test_trailing_null_is_not_stripped_as_whitespace():
    arr = np.array(["x\0", "\0 ", " \0", "x\0 \t"],
                   dtype=StringDType())

    assert_array_equal(
            np.strings.rstrip(arr),
            np.array(["x\0", "\0", " \0", "x\0"], dtype=StringDType()))
    assert_array_equal(
            np.strings.strip(arr),
            np.array(["x\0", "\0", "\0", "x\0"], dtype=StringDType()))

