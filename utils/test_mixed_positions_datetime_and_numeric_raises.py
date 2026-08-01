
def test_mixed_positions_datetime_and_numeric_raises():
    """Test that mixed datetime and numeric positions
    with float widths raise TypeError.
    """
    fig, ax = plt.subplots()
    positions = [datetime.datetime(2020, 1, 1), 2.0]
    widths = [0.5, 1.0]
    with pytest.raises(TypeError,
                       match=("datetime/date 'position' values require "
                              "timedelta 'widths'")):
        ax.violin(violin_plot_stats(), positions=positions, widths=widths)

