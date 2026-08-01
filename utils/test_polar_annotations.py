
def test_polar_annotations():
    # You can specify the xypoint and the xytext in different positions and
    # coordinate systems, and optionally turn on a connecting line and mark the
    # point with a marker.  Annotations work on polar axes too.  In the example
    # below, the xy point is in native coordinates (xycoords defaults to
    # 'data').  For a polar axes, this is in (theta, radius) space.  The text
    # in this example is placed in the fractional figure coordinate system.
    # Text keyword args like horizontal and vertical alignment are respected.

    # Setup some data
    r = np.arange(0.0, 1.0, 0.001)
    theta = 2.0 * 2.0 * np.pi * r

    fig = plt.figure()
    ax = fig.add_subplot(polar=True)
    line, = ax.plot(theta, r, color='#ee8d18', lw=3)
    line, = ax.plot((0, 0), (0, 1), color="#0000ff", lw=1)

    ind = 800
    thisr, thistheta = r[ind], theta[ind]
    ax.plot([thistheta], [thisr], 'o')
    ax.annotate('a polar annotation',
                xy=(thistheta, thisr),  # theta, radius
                xytext=(0.05, 0.05),    # fraction, fraction
                textcoords='figure fraction',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='left',
                verticalalignment='baseline',
                )

    ax.tick_params(axis='x', tick1On=True, tick2On=True, direction='out')

