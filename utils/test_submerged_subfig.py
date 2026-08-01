
def test_submerged_subfig():
    """
    Test that the submerged margin logic does not get called multiple times
    on same axes if it is already in a subfigure
    """
    fig = plt.figure(figsize=(4, 5), layout='constrained')
    figures = fig.subfigures(3, 1)
    axs = []
    for f in figures.flatten():
        gs = f.add_gridspec(2, 2)
        for i in range(2):
            axs += [f.add_subplot(gs[i, 0])]
            axs[-1].plot()
        f.add_subplot(gs[:, 1]).plot()
    fig.draw_without_rendering()
    for ax in axs[1:]:
        assert np.allclose(ax.get_position().bounds[-1],
                           axs[0].get_position().bounds[-1], atol=1e-6)

