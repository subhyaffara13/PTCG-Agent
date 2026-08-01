
def test_axesgrid_colorbar_log_smoketest():
    fig = plt.figure()
    grid = AxesGrid(fig, 111,  # modified to be only subplot
                    nrows_ncols=(1, 1),
                    label_mode="L",
                    cbar_location="top",
                    cbar_mode="single",
                    )

    Z = 10000 * np.random.rand(10, 10)
    im = grid[0].imshow(Z, interpolation="nearest", norm=LogNorm())

    grid.cbar_axes[0].colorbar(im)

