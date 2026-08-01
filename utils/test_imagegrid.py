
def test_imagegrid():
    fig = plt.figure()
    grid = ImageGrid(fig, 111, nrows_ncols=(1, 1))
    ax = grid[0]
    im = ax.imshow([[1, 2]], norm=mpl.colors.LogNorm())
    cb = ax.cax.colorbar(im)
    assert isinstance(cb.locator, mticker.LogLocator)

