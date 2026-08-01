
def test_use_colorizer_keyword():
    # test using the colorizer keyword
    np.random.seed(0)
    rand_x = np.random.random(100)
    rand_y = np.random.random(100)
    c = np.arange(25, dtype='float32').reshape((5, 5))

    fig, axes = plt.subplots(3, 4)
    norm = mpl.colors.Normalize(4, 20)
    cl = mpl.colorizer.Colorizer(norm=norm, cmap='RdBu')

    axes[0, 0].scatter(c, c, c=c, colorizer=cl)
    axes[0, 1].hexbin(rand_x, rand_y, colorizer=cl, gridsize=(2, 2))
    axes[0, 2].imshow(c, colorizer=cl)
    axes[0, 3].pcolor(c, colorizer=cl)
    axes[1, 0].pcolormesh(c, colorizer=cl)
    axes[1, 1].pcolorfast(c, colorizer=cl)  # style = image
    axes[1, 2].pcolorfast((0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 5, 6),  c,
                          colorizer=cl)  # style = pcolorimage
    axes[1, 3].pcolorfast(c.T, c, c[:4, :4], colorizer=cl)  # style = quadmesh
    axes[2, 0].contour(c, colorizer=cl)
    axes[2, 1].contourf(c, colorizer=cl)
    axes[2, 2].tricontour(c.T.ravel(), c.ravel(), c.ravel(), colorizer=cl)
    axes[2, 3].tricontourf(c.T.ravel(), c.ravel(), c.ravel(), colorizer=cl)

    fig.figimage(np.repeat(np.repeat(c, 15, axis=0), 15, axis=1), colorizer=cl)
    remove_ticks_and_titles(fig)

