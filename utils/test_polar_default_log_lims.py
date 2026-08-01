
def test_polar_default_log_lims():
    plt.subplot(projection='polar')
    ax = plt.gca()
    ax.set_rscale('log')
    assert ax.get_rmin() > 0

