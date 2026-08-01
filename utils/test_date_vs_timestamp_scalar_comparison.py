
def test_date_vs_timestamp_scalar_comparison():
    # GH#62157 match non-pyarrow behavior
    ser = pd.Series(["2016-01-01"], dtype="date32[pyarrow]")
    ser2 = ser.astype("timestamp[ns][pyarrow]")

    ts = ser2[0]
    dt = ser[0]

    # date dtype don't match a Timestamp object
    assert not (ser == ts).any()
    assert not (ts == ser).any()

    # timestamp dtype doesn't match date object
    assert not (ser2 == dt).any()
    assert not (dt == ser2).any()

