
def test_constrained_layout4():
    """Test constrained_layout for a single colorbar with subplots"""

    fig, axs = plt.subplots(2, 2, layout="constrained")
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=24)
    fig.colorbar(pcm, ax=axs, pad=0.01, shrink=0.6)

