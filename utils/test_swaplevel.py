
def test_swaplevel(obj):
    index = MultiIndex.from_tuples([(1, 1), (1, 2), (2, 1)], names=["one", "two"])
    obj.index = index
    obj_orig = obj.copy()
    obj2 = obj.swaplevel()
    assert np.shares_memory(obj2.values, obj.values)

    obj2.iloc[0] = 0
    assert not np.shares_memory(obj2.values, obj.values)
    tm.assert_equal(obj, obj_orig)

