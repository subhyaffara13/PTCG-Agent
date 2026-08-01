
def test_datetime_positions_with_float_widths_raises():
    """Test that datetime positions with float widths raise TypeError."""
    fig, ax = plt.subplots()
    positions = [datetime.datetime(2020, 1, 1), datetime.datetime(2021, 1, 1)]
    widths = [0.5, 1.0]
    with pytest.raises(TypeError,
                       match=("datetime/date 'position' values require "
                              "timedelta 'widths'")):
        ax.violin(violin_plot_stats(), positions=positions, widths=widths)

