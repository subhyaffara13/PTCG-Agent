
def test_scale3d_persists_after_plot():
    """Scale should persist after adding plot data."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set(xscale='log', yscale='log', zscale='log')
    ax.plot(*_make_log_data())
    assert (ax.get_xscale(), ax.get_yscale(), ax.get_zscale()) == ('log',) * 3

