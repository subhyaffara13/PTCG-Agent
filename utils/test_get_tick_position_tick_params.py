
def test_get_tick_position_tick_params():
    """Test that get_tick_position() correctly picks up tick_params()."""
    ax = plt.figure().add_subplot()
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False,
                   right=True, labelright=True, left=False, labelleft=False)
    assert ax.xaxis.get_ticks_position() == "top"
    assert ax.yaxis.get_ticks_position() == "right"

