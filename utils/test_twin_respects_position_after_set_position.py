
def test_twin_respects_position_after_set_position(twin):
    fig, ax = plt.subplots()

    ax.set_position([0.2, 0.2, 0.5, 0.5])
    ax2 = getattr(ax, f"twin{twin}")()

    assert_allclose(ax.get_position(original=True).bounds,
                    ax2.get_position(original=True).bounds)

    assert_allclose(ax.get_position(original=False).bounds,
                    ax2.get_position(original=False).bounds)

