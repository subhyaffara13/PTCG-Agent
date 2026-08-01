
def test_clim():
    ax = plt.figure().add_subplot()
    for plot_method in [
            partial(ax.scatter, range(3), range(3), c=range(3)),
            partial(ax.imshow, [[0, 1], [2, 3]]),
            partial(ax.pcolor,  [[0, 1], [2, 3]]),
            partial(ax.pcolormesh, [[0, 1], [2, 3]]),
            partial(ax.pcolorfast, [[0, 1], [2, 3]]),
    ]:
        clim = (7, 8)
        norm = plot_method(clim=clim).norm
        assert (norm.vmin, norm.vmax) == clim

