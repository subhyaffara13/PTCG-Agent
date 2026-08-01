
def test_date2num_NaT(dtype):
    t0 = datetime.datetime(2017, 1, 1, 0, 1, 1)
    tmpl = [mdates.date2num(t0), np.nan]
    tnp = np.array([t0, 'NaT'], dtype=dtype)
    nptime = mdates.date2num(tnp)
    np.testing.assert_array_equal(tmpl, nptime)

