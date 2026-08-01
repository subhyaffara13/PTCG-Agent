
def test_twin_keeps_layout_participation_for_layout_managed_axes(twin):
    fig, ax = plt.subplots()

    ax2 = getattr(ax, f"twin{twin}")()

    assert ax.get_in_layout()
    assert ax2.get_in_layout()

