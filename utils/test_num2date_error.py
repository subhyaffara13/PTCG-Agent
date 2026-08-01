
def test_num2date_error(val):
    with pytest.raises(ValueError, match=f"Date ordinal {val} converts"):
        mdates.num2date(val)

