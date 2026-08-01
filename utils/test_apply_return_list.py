
def test_apply_return_list():
    df = DataFrame({"a": [1, 2], "b": [2, 3]})
    result = df.apply(lambda x: [x.values])
    expected = DataFrame({"a": [[1, 2]], "b": [[2, 3]]})
    tm.assert_frame_equal(result, expected)

