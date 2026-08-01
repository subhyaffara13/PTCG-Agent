
def test_get_tick_position_rcParams():
    """Test that get_tick_position() correctly picks up rcParams tick positions."""
    plt.rcParams.update({
        "xtick.top": 1, "xtick.labeltop": 1, "xtick.bottom": 0, "xtick.labelbottom": 0,
        "ytick.right": 1, "ytick.labelright": 1, "ytick.left": 0, "ytick.labelleft": 0,
    })
    ax = plt.figure().add_subplot()
    assert ax.xaxis.get_ticks_position() == "top"
    assert ax.yaxis.get_ticks_position() == "right"

