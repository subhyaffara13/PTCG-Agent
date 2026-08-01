
def test_colorbar_pos():
    num_plots = 2
    fig, axs = plt.subplots(1, num_plots, figsize=(4, 5),
                            constrained_layout=True,
                            subplot_kw={'projection': '3d'})
    for ax in axs:
        p_tri = ax.plot_trisurf(np.random.randn(5), np.random.randn(5),
                                np.random.randn(5))

    cbar = plt.colorbar(p_tri, ax=axs, orientation='horizontal')

    fig.canvas.draw()
    # check that actually on the bottom
    assert cbar.ax.get_position().extents[1] < 0.2

