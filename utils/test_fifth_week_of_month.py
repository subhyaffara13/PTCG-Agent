
def test_fifth_week_of_month():
    # see gh-9425
    #
    # Only supports freq up to WOM-4.
    msg = "Invalid frequency: WOM-5MON"

    with pytest.raises(ValueError, match=msg):
        date_range("2014-01-01", freq="WOM-5MON")

