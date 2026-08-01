
def test_ensure_string_array_list_of_lists():
    # GH#61155: ensure list of lists doesn't get converted to string
    arr = [list("test"), list("word")]
    result = lib.ensure_string_array(arr)

    # Each item in result should still be a list, not a stringified version
    expected = np.array(["['t', 'e', 's', 't']", "['w', 'o', 'r', 'd']"], dtype=object)
    tm.assert_numpy_array_equal(result, expected)

