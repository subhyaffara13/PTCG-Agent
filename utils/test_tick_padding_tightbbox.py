
def test_tick_padding_tightbbox():
    """Test that tick padding gets turned off if axis is off"""
    plt.rcParams["xtick.direction"] = "out"
    plt.rcParams["ytick.direction"] = "out"
    fig, ax = plt.subplots()
    bb = ax.get_tightbbox(fig.canvas.get_renderer())
    ax.axis('off')
    bb2 = ax.get_tightbbox(fig.canvas.get_renderer())
    assert bb.x0 < bb2.x0
    assert bb.y0 < bb2.y0

