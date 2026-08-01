
def test_between_time(obj):
    obj.index = date_range("2018-04-09", periods=2, freq="1D20min")
    obj_orig = obj.copy()
    obj2 = obj.between_time("0:00", "1:00")
    assert np.shares_memory(obj2.values, obj.values)

    obj2.iloc[0] = 0
    assert not np.shares_memory(obj2.values, obj.values)
    tm.assert_equal(obj, obj_orig)

