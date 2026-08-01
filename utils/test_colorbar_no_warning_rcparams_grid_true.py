
def test_colorbar_no_warning_rcparams_grid_true():
    # github issue #21723 - If mpl style has 'axes.grid' = True,
    # fig.colorbar raises a warning about Auto-removal of grids
    # by pcolor() and pcolormesh(). This is fixed by PR #22216.
    plt.rcParams['axes.grid'] = True
    fig, ax = plt.subplots()
    ax.grid(False)
    im = ax.pcolormesh([0, 1], [0, 1], [[1]])
    # make sure that no warning is raised by fig.colorbar
    fig.colorbar(im)

