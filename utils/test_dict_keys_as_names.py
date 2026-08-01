
def test_dict_keys_as_names(all_parsers):
    # GH: 36928
    data = "1,2"

    keys = {"a": int, "b": int}.keys()
    parser = all_parsers

    result = parser.read_csv(StringIO(data), names=keys)
    expected = DataFrame({"a": [1], "b": [2]})
    tm.assert_frame_equal(result, expected)

