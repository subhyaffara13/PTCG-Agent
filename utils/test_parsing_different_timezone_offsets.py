
def test_parsing_different_timezone_offsets():
    # see gh-17697
    data = ["2015-11-18 15:30:00+05:30", "2015-11-18 15:30:00+06:30"]
    data = np.array(data, dtype=object)

    msg = "Mixed timezones detected. Pass utc=True in to_datetime"
    with pytest.raises(ValueError, match=msg):
        tslib.array_to_datetime(data)

