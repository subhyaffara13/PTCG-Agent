
def test_date_empty():
    # make sure we do the right thing when told to plot dates even
    # if no date data has been presented, cf
    # http://sourceforge.net/tracker/?func=detail&aid=2850075&group_id=80706&atid=560720
    fig, ax = plt.subplots()
    ax.xaxis_date()
    fig.draw_without_rendering()
    np.testing.assert_allclose(ax.get_xlim(),
                               [mdates.date2num(np.datetime64('1970-01-01')),
                                mdates.date2num(np.datetime64('1970-01-02'))])

    mdates._reset_epoch_test_example()
    mdates.set_epoch('0000-12-31')
    fig, ax = plt.subplots()
    ax.xaxis_date()
    fig.draw_without_rendering()
    np.testing.assert_allclose(ax.get_xlim(),
                               [mdates.date2num(np.datetime64('1970-01-01')),
                                mdates.date2num(np.datetime64('1970-01-02'))])
    mdates._reset_epoch_test_example()

