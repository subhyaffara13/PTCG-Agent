
def test_datetime_positions_with_scalar_float_width_raises():
    """Test that datetime positions with scalar float width raise TypeError."""
    fig, ax = plt.subplots()
    positions = [datetime.datetime(2020, 1, 1), datetime.datetime(2021, 1, 1)]
    widths = 0.75
    with pytest.raises(TypeError,
                       match=("datetime/date 'position' values require "
                              "timedelta 'widths'")):
        ax.violin(violin_plot_stats(), positions=positions, widths=widths)

