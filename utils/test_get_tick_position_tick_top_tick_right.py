
def test_get_tick_position_tick_top_tick_right():
    """Test that get_tick_position() correctly picks up tick_top() / tick_right()."""
    ax = plt.figure().add_subplot()
    ax.xaxis.tick_top()
    ax.yaxis.tick_right()
    assert ax.xaxis.get_ticks_position() == "top"
    assert ax.yaxis.get_ticks_position() == "right"

