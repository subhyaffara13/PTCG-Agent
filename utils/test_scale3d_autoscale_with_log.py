
def test_scale3d_autoscale_with_log():
    """Autoscale should work correctly with log scale."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set(xscale='log', yscale='log', zscale='log')
    ax.scatter([1, 10, 100], [1, 10, 100], [1, 10, 100])

    # All limits should be positive
    for name, lim in [('x', ax.get_xlim()), ('y', ax.get_ylim()),
                      ('z', ax.get_zlim())]:
        assert lim[0] > 0, f"{name} lower limit should be positive"
        assert lim[1] > 0, f"{name} upper limit should be positive"

