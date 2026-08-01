
def test_formatter_ticker():
    import matplotlib.testing.jpl_units as units
    units.register()

    # This should not affect the tick size.  (Tests issue #543)
    matplotlib.rcParams['lines.markeredgewidth'] = 30

    # This essentially test to see if user specified labels get overwritten
    # by the auto labeler functionality of the axes.
    xdata = [x*units.sec for x in range(10)]
    ydata1 = [(1.5*y - 0.5)*units.km for y in range(10)]
    ydata2 = [(1.75*y - 1.0)*units.km for y in range(10)]

    ax = plt.figure().subplots()
    ax.set_xlabel("x-label 001")

    ax = plt.figure().subplots()
    ax.set_xlabel("x-label 001")
    ax.plot(xdata, ydata1, color='blue', xunits="sec")

    ax = plt.figure().subplots()
    ax.set_xlabel("x-label 001")
    ax.plot(xdata, ydata1, color='blue', xunits="sec")
    ax.set_xlabel("x-label 003")

    ax = plt.figure().subplots()
    ax.plot(xdata, ydata1, color='blue', xunits="sec")
    ax.plot(xdata, ydata2, color='green', xunits="hour")
    ax.set_xlabel("x-label 004")

    # See SF bug 2846058
    # https://sourceforge.net/tracker/?func=detail&aid=2846058&group_id=80706&atid=560720
    ax = plt.figure().subplots()
    ax.plot(xdata, ydata1, color='blue', xunits="sec")
    ax.plot(xdata, ydata2, color='green', xunits="hour")
    ax.set_xlabel("x-label 005")
    ax.autoscale_view()

