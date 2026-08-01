
def test_sort_values(obj, kwargs):
    obj_orig = obj.copy()
    obj2 = obj.sort_values(**kwargs)
    assert np.shares_memory(get_array(obj2, "a"), get_array(obj, "a"))

    # mutating df triggers a copy-on-write for the column / block
    obj2.iloc[0] = 0
    assert not np.shares_memory(get_array(obj2, "a"), get_array(obj, "a"))
    tm.assert_equal(obj, obj_orig)

