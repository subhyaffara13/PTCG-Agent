
def test_setitem_raises_length():
    arr = PeriodArray(np.arange(3), dtype="period[D]")
    with pytest.raises(ValueError, match="length"):
        arr[[0, 1]] = [pd.Period("2000", freq="D")]

