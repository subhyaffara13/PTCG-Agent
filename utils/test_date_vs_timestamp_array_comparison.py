
def test_date_vs_timestamp_array_comparison():
    # GH#62157 match non-pyarrow behavior
    # GH#
    ser = pd.Series(["2016-01-01"], dtype="date32[pyarrow]")
    ser2 = ser.astype("timestamp[ns][pyarrow]")
    ser3 = ser.astype("datetime64[ns]")

    assert not (ser == ser2).any()
    assert not (ser2 == ser).any()
    assert (ser != ser2).all()
    assert (ser2 != ser).all()

    assert not (ser == ser3).any()
    assert not (ser3 == ser).any()
    assert (ser != ser3).all()
    assert (ser3 != ser).all()

