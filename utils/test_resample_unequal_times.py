
def test_resample_unequal_times(unit):
    # #1772
    start = datetime(1999, 3, 1, 5)
    # end hour is less than start
    end = datetime(2012, 7, 31, 4)
    bad_ind = date_range(start, end, freq="30min").as_unit(unit)
    df = DataFrame({"close": 1}, index=bad_ind)

    # it works!
    df.resample("YS").sum()

