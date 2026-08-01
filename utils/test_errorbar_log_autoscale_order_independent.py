
def test_errorbar_log_autoscale_order_independent():
    x = 10 ** np.array([18, 18.1, 18.2, 18.3])
    y = np.array([100, 80, 60, 30])
    yerr = np.ones_like(y) * 10

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.errorbar(x, y, yerr=yerr)

    ax2.errorbar(x, y, yerr=yerr)
    ax2.set_xscale("log")
    ax2.set_yscale("log")

    assert_allclose(ax1.get_xlim(), ax2.get_xlim())
    assert_allclose(ax1.get_ylim(), ax2.get_ylim())

