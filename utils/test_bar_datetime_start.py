
def test_bar_datetime_start():
    """test that tickers are correct for datetimes"""
    start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'),
                      np.datetime64('2012-01-15')])
    stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'),
                     np.datetime64('2012-02-12')])

    fig, ax = plt.subplots()
    ax.bar([0, 1, 3], height=stop-start, bottom=start)
    assert isinstance(ax.yaxis.get_major_formatter(), mdates.AutoDateFormatter)

    fig, ax = plt.subplots()
    ax.barh([0, 1, 3], width=stop-start, left=start)
    assert isinstance(ax.xaxis.get_major_formatter(), mdates.AutoDateFormatter)

