
def test_setitem_raises_type():
    arr = PeriodArray(np.arange(3), dtype="period[D]")
    with pytest.raises(TypeError, match="int"):
        arr[0] = 1

