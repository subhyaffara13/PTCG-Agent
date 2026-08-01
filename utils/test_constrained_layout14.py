
def test_constrained_layout14():
    """Test that padding works."""
    fig, axs = plt.subplots(2, 2, layout="constrained")
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=12)
        fig.colorbar(pcm, ax=ax, shrink=0.6, aspect=20., pad=0.02)
    fig.get_layout_engine().set(
            w_pad=3./72., h_pad=3./72.,
            hspace=0.2, wspace=0.2)

