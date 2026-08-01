
def test_unknown_tz_raises():
    # GH#18702, GH#51476
    dtstr = "2014 Jan 9 05:15 FAKE"
    msg = '.*un-recognized timezone "FAKE".'
    with pytest.raises(ValueError, match=msg):
        Timestamp(dtstr)

    with pytest.raises(ValueError, match=msg):
        to_datetime(dtstr)
    with pytest.raises(ValueError, match=msg):
        to_datetime([dtstr])

