
def test_get_day_of_year_numeric(date_tuple, expected):
    assert ccalendar.get_day_of_year(*date_tuple) == expected

