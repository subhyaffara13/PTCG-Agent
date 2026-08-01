
def test_td64_sum_empty(skipna):
    # GH#37151
    ser = Series([], dtype="timedelta64[ns]")

    result = ser.sum(skipna=skipna)
    assert isinstance(result, pd.Timedelta)
    assert result == pd.Timedelta(0)

