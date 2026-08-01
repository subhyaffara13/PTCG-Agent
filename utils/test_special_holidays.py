
def test_special_holidays(name, kwargs):
    base_date = [datetime(2012, 5, 28)]
    holiday = Holiday(name, **kwargs)

    start_date = datetime(2011, 1, 1)
    end_date = datetime(2020, 12, 31)

    assert base_date == holiday.dates(start_date, end_date)

