
def test_dt_correct_iso_8601_year_week_and_day(input_date_tuple, expected_iso_tuple):
    result = ccalendar.get_iso_calendar(*input_date_tuple)
    expected_from_date_isocalendar = date(*input_date_tuple).isocalendar()
    assert result == expected_from_date_isocalendar
    assert result == expected_iso_tuple

