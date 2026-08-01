
def test_datetime64_in_list():
    dt = [np.datetime64('2000-01-01'), np.datetime64('2001-01-01')]
    dn = mdates.date2num(dt)
    # convert fixed values from old to new epoch
    t = (np.array([730120.,  730486.]) +
         mdates.date2num(np.datetime64('0000-12-31')))
    np.testing.assert_equal(dn, t)

