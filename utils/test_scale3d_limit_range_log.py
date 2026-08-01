
def test_scale3d_limit_range_log(axis):
    """Log scale should warn when setting non-positive limits."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    getattr(ax, f'set_{axis}scale')('log')

    # Setting non-positive limits should warn
    with pytest.warns(UserWarning, match="non-positive"):
        getattr(ax, f'set_{axis}lim')(-10, 100)

