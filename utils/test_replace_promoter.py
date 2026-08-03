import itertools

def test_replace_promoter():
    arg = ["Hello, planet!", "planet, Hello!"]
    old = "planet"
    new = "world"
    answer = ["Hello, world!", "world, Hello!"]
    for dtypes in itertools.product("TU", repeat=3):
        if dtypes == ("U", "U", "U"):
            continue
        answer_arr = np.strings.replace(
            np.array(arg, dtype=dtypes[0]),
            np.array(old, dtype=dtypes[1]),
            np.array(new, dtype=dtypes[2]),
        )
        assert_array_equal(answer_arr, answer)
        assert answer_arr.dtype.char == "T"

