
def test_string_to_cfloat_cast_distinct_components(typename):
    inp = np.array(
        ["1.25+0.5j", "2.75-3.5j", "-3.125+4.25j", "27000-8j"],
        dtype="T",
    )
    expected = np.array(
        [1.25 + 0.5j, 2.75 - 3.5j, -3.125 + 4.25j, 2.7e4 - 8j],
        dtype=typename,
    )
    assert_array_equal(inp.astype(typename), expected)

