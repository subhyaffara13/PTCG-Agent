
def test_from_product_respects_none_names():
    # GH27292
    a = Series([1, 2, 3], name="foo")
    b = Series(["a", "b"], name="bar")

    result = MultiIndex.from_product([a, b], names=None)
    expected = MultiIndex(
        levels=[[1, 2, 3], ["a", "b"]],
        codes=[[0, 0, 1, 1, 2, 2], [0, 1, 0, 1, 0, 1]],
        names=None,
    )
    tm.assert_index_equal(result, expected)

