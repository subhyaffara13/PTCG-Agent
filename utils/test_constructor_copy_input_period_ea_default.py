
def test_constructor_copy_input_period_ea_default():
    # GH 63388
    arr = array(["2020-01-01", "2020-01-02"], dtype="period[D]")
    idx = PeriodIndex(arr)
    assert not tm.shares_memory(arr, idx.array)

