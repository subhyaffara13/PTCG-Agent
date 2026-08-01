
def test_constrained_layout5():
    """
    Test constrained_layout for a single colorbar with subplots,
    colorbar bottom
    """

    fig, axs = plt.subplots(2, 2, layout="constrained")
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=24)
    fig.colorbar(pcm, ax=axs,
                 use_gridspec=False, pad=0.01, shrink=0.6,
                 location='bottom')

