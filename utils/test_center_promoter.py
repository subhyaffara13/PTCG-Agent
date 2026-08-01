
def test_center_promoter():
    arg = ["Hello", "planet!"]
    fillchar = "/"
    for dtypes in [("T", "U"), ("U", "T")]:
        answer = np.strings.center(
            np.array(arg, dtype=dtypes[0]), 9, np.array(fillchar, dtype=dtypes[1])
        )
        assert_array_equal(answer, ["//Hello//", "/planet!/"])
        assert answer.dtype.char == "T"

