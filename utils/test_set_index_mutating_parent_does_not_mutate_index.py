
def test_set_index_mutating_parent_does_not_mutate_index():
    df = DataFrame({"a": [1, 2, 3], "b": 1})
    result = df.set_index("a")
    expected = result.copy()

    df.iloc[0, 0] = 100
    tm.assert_frame_equal(result, expected)

