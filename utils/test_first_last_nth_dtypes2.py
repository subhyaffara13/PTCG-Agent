
def test_first_last_nth_dtypes2():
    # GH 2763, first/last shifting dtypes
    idx = list(range(10))
    idx.append(9)
    ser = Series(data=range(11), index=idx, name="IntCol")
    assert ser.dtype == "int64"
    f = ser.groupby(level=0).first()
    assert f.dtype == "int64"

