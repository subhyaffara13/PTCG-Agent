
def test_lognorm_levels(n_levels):
    x, y = np.mgrid[1:10:0.1, 1:10:0.1]
    data = np.abs(np.sin(x)*np.exp(y))

    fig, ax = plt.subplots()
    im = ax.contour(x, y, data, norm=LogNorm(), levels=n_levels)
    fig.colorbar(im, ax=ax)

    levels = im.levels
    visible_levels = levels[(levels <= data.max()) & (levels >= data.min())]
    # levels parameter promises "no more than n+1 "nice" contour levels "
    assert len(visible_levels) <= n_levels + 1

