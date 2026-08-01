
def test_from_product_empty_two_levels(first, second):
    names = ["A", "B"]
    result = MultiIndex.from_product([first, second], names=names)
    expected = MultiIndex(levels=[first, second], codes=[[], []], names=names)
    tm.assert_index_equal(result, expected)

