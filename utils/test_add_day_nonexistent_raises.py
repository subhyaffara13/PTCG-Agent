
def test_add_day_nonexistent_raises():
    # https://github.com/pandas-dev/pandas/issues/41943#issuecomment-1466978225

    ts = Timestamp("2015-03-28T2:30", tz="Europe/Warsaw")

    msg = "is a nonexistent time due to daylight savings time"
    with pytest.raises(ValueError, match=msg):
        ts + Day(1)

