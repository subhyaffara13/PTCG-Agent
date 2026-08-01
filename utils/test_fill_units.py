
def test_fill_units():
    import matplotlib.testing.jpl_units as units
    units.register()

    # generate some data
    t = units.Epoch("ET", dt=datetime.datetime(2009, 4, 27))
    value = 10.0 * units.deg
    day = units.Duration("ET", 24.0 * 60.0 * 60.0)
    dt = np.arange('2009-04-27', '2009-04-29', dtype='datetime64[D]')
    dtn = mdates.date2num(dt)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    ax1.plot([t], [value], yunits='deg', color='red')
    ind = [0, 0, 1, 1]
    ax1.fill(dtn[ind], [0.0, 0.0, 90.0, 0.0], 'b')

    ax2.plot([t], [value], yunits='deg', color='red')
    ax2.fill([t, t, t + day, t + day],
             [0.0, 0.0, 90.0, 0.0], 'b')

    ax3.plot([t], [value], yunits='deg', color='red')
    ax3.fill(dtn[ind],
             [0 * units.deg, 0 * units.deg, 90 * units.deg, 0 * units.deg],
             'b')

    ax4.plot([t], [value], yunits='deg', color='red')
    ax4.fill([t, t, t + day, t + day],
             [0 * units.deg, 0 * units.deg, 90 * units.deg, 0 * units.deg],
             facecolor="blue")
    fig.autofmt_xdate()

