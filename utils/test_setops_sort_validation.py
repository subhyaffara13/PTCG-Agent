
def test_setops_sort_validation(method):
    idx1 = MultiIndex.from_product([["a", "b"], [1, 2]])
    idx2 = MultiIndex.from_product([["b", "c"], [1, 2]])

    with pytest.raises(ValueError, match="The 'sort' keyword only takes"):
        getattr(idx1, method)(idx2, sort=2)

    # sort=True is supported as of GH#?
    getattr(idx1, method)(idx2, sort=True)

