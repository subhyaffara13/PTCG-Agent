
def test_as_unit_date_raises():
    # as_unit should raise for date types
    ser = pd.Series([1, 2], dtype=ArrowDtype(pa.date32()))
    with pytest.raises(NotImplementedError, match="as_unit not implemented"):
        ser.dt.as_unit("ns")

