
def test_datetime_positions_with_datetime64():
    """Test that datetime positions with float widths raise TypeError."""
    fig, ax = plt.subplots()
    positions = [np.datetime64('2020-01-01'), np.datetime64('2021-01-01')]
    widths = [0.5, 1.0]
    with pytest.raises(TypeError,
                       match=("np.datetime64 'position' values require "
                              "np.timedelta64 'widths'")):
        ax.violin(violin_plot_stats(), positions=positions, widths=widths)

