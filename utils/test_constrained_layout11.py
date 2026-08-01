
def test_constrained_layout11():
    """Test for multiple nested gridspecs"""

    fig = plt.figure(layout="constrained", figsize=(13, 3))
    gs0 = gridspec.GridSpec(1, 2, figure=fig)
    gsl = gridspec.GridSpecFromSubplotSpec(1, 2, gs0[0])
    gsl0 = gridspec.GridSpecFromSubplotSpec(2, 2, gsl[1])
    ax = fig.add_subplot(gs0[1])
    example_plot(ax, fontsize=9)
    axs = []
    for gs in gsl0:
        ax = fig.add_subplot(gs)
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=9)
    fig.colorbar(pcm, ax=axs, shrink=0.6, aspect=70.)
    ax = fig.add_subplot(gsl[0])
    example_plot(ax, fontsize=9)

