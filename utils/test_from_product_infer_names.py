
def test_from_product_infer_names(a, b, expected_names):
    # GH27292
    result = MultiIndex.from_product([a, b])
    expected = MultiIndex(
        levels=[[1, 2, 3], ["a", "b"]],
        codes=[[0, 0, 1, 1, 2, 2], [0, 1, 0, 1, 0, 1]],
        names=expected_names,
    )
    tm.assert_index_equal(result, expected)

