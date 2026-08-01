
def test_isocalendar(dt):
    expected = dt.isocalendar()
    result = ccalendar.get_iso_calendar(dt.year, dt.month, dt.day)
    assert result == expected

