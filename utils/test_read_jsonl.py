
def test_read_jsonl():
    # GH9180
    result = read_json(StringIO('{"a": 1, "b": 2}\n{"b":2, "a" :1}\n'), lines=True)
    expected = DataFrame([[1, 2], [1, 2]], columns=["a", "b"])
    tm.assert_frame_equal(result, expected)

