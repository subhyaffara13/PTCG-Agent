
def test_dt_to_pydatetime_date_error(date_type):
    # GH 52812
    ser = pd.Series(
        [date(2022, 12, 31)],
        dtype=ArrowDtype(getattr(pa, f"date{date_type}")()),
    )
    with pytest.raises(ValueError, match="to_pydatetime cannot be called with"):
        ser.dt.to_pydatetime()

