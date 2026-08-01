
def test_set_names_with_nlevel_1(inplace):
    # GH 21149
    # Ensure that .set_names for MultiIndex with
    # nlevels == 1 does not raise any errors
    expected = MultiIndex(levels=[[0, 1]], codes=[[0, 1]], names=["first"])
    m = MultiIndex.from_product([[0, 1]])
    result = m.set_names("first", level=0, inplace=inplace)

    if inplace:
        result = m

    tm.assert_index_equal(result, expected)

