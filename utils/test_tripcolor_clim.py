
def test_tripcolor_clim():
    np.random.seed(19680801)
    a, b, c = np.random.rand(10), np.random.rand(10), np.random.rand(10)

    ax = plt.figure().add_subplot()
    clim = (0.25, 0.75)
    norm = ax.tripcolor(a, b, c, clim=clim).norm
    assert (norm.vmin, norm.vmax) == clim

