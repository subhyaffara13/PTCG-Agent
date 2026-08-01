
def test_basic_getitem_dt64tz_values():
    # GH12089
    # with tz for values
    ser = Series(
        date_range("2011-01-01", periods=3, tz="US/Eastern"), index=["a", "b", "c"]
    )
    expected = Timestamp("2011-01-01", tz="US/Eastern")
    result = ser.loc["a"]
    assert result == expected
    result = ser.iloc[0]
    assert result == expected
    result = ser["a"]
    assert result == expected

