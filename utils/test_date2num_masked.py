
def test_date2num_masked():
    # Without tzinfo
    base = datetime.datetime(2022, 12, 15)
    dates = np.ma.array([base + datetime.timedelta(days=(2 * i))
                         for i in range(7)], mask=[0, 1, 1, 0, 0, 0, 1])
    npdates = mdates.date2num(dates)
    np.testing.assert_array_equal(np.ma.getmask(npdates),
                                  (False, True, True, False, False, False,
                                   True))

    # With tzinfo
    base = datetime.datetime(2022, 12, 15, tzinfo=mdates.UTC)
    dates = np.ma.array([base + datetime.timedelta(days=(2 * i))
                         for i in range(7)], mask=[0, 1, 1, 0, 0, 0, 1])
    npdates = mdates.date2num(dates)
    np.testing.assert_array_equal(np.ma.getmask(npdates),
                                  (False, True, True, False, False, False,
                                   True))

