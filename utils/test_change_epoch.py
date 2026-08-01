
def test_change_epoch():
    date = np.datetime64('2000-01-01')

    # use private method to clear the epoch and allow it to be set...
    mdates._reset_epoch_test_example()
    mdates.get_epoch()  # Set default.

    with pytest.raises(RuntimeError):
        # this should fail here because there is a sentinel on the epoch
        # if the epoch has been used then it cannot be set.
        mdates.set_epoch('0000-01-01')

    mdates._reset_epoch_test_example()
    mdates.set_epoch('1970-01-01')
    dt = (date - np.datetime64('1970-01-01')).astype('datetime64[D]')
    dt = dt.astype('int')
    np.testing.assert_equal(mdates.date2num(date), float(dt))

    mdates._reset_epoch_test_example()
    mdates.set_epoch('0000-12-31')
    np.testing.assert_equal(mdates.date2num(date), 730120.0)

    mdates._reset_epoch_test_example()
    mdates.set_epoch('1970-01-01T01:00:00')
    np.testing.assert_allclose(mdates.date2num(date), dt - 1./24.)
    mdates._reset_epoch_test_example()
    mdates.set_epoch('1970-01-01T00:00:00')
    np.testing.assert_allclose(
        mdates.date2num(np.datetime64('1970-01-01T12:00:00')),
        0.5)

