
def test_join_self(idx, join_type):
    result = idx.join(idx, how=join_type)
    expected = idx
    if join_type == "outer":
        expected = expected.sort_values()
    tm.assert_index_equal(result, expected)

