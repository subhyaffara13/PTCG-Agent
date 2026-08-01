
def test_twin_stays_aligned_after_constrained_layout(twin):
    fig, ax = plt.subplots(constrained_layout=True)

    ax.set_position([0.2, 0.2, 0.5, 0.5])
    ax2 = getattr(ax, f"twin{twin}")()

    fig.canvas.draw()

    assert_allclose(ax.get_position().bounds, ax2.get_position().bounds)

