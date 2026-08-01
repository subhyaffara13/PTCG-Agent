
def test_name_mi_with_dict_like(func, rename_dict, exp_names):
    # GH#20421
    mi = MultiIndex.from_arrays([[1, 2], [3, 4]], names=["x", "y"])
    result = getattr(mi, func)(rename_dict)
    expected = MultiIndex.from_arrays([[1, 2], [3, 4]], names=exp_names)
    tm.assert_index_equal(result, expected)

