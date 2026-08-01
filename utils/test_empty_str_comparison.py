
def test_empty_str_comparison(power, string_size):
    # GH 37348
    a = np.array(range(10**power))
    right = pd.DataFrame(a, dtype=np.int64)
    left = " " * string_size

    result = right == left
    expected = pd.DataFrame(np.zeros(right.shape, dtype=bool))
    tm.assert_frame_equal(result, expected)

