
def test_append_one_nonempty_preserve_step():
    expected = RangeIndex(0, -1, -1)
    result = RangeIndex(0).append([expected])
    tm.assert_index_equal(result, expected, exact=True)

