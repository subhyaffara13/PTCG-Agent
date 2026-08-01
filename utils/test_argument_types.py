
def test_argument_types(transform):
    start_date = datetime(2011, 1, 1)
    end_date = datetime(2020, 12, 31)

    holidays = USThanksgivingDay.dates(start_date, end_date)
    holidays2 = USThanksgivingDay.dates(transform(start_date), transform(end_date))
    tm.assert_index_equal(holidays, holidays2)

