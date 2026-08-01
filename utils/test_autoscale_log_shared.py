
def test_autoscale_log_shared():
    # related to github #7587
    # array starts at zero to trigger _minpos handling
    x = np.arange(100, dtype=float)
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.loglog(x, x)
    ax2.semilogx(x, x)
    ax1.autoscale(tight=True)
    ax2.autoscale(tight=True)
    plt.draw()
    lims = (x[1], x[-1])
    assert_allclose(ax1.get_xlim(), lims)
    assert_allclose(ax1.get_ylim(), lims)
    assert_allclose(ax2.get_xlim(), lims)
    assert_allclose(ax2.get_ylim(), (x[0], x[-1]))

