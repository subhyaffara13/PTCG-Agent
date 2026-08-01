
def test_wrong_use_colorizer():
    # test using the colorizer keyword and norm or cmap
    np.random.seed(0)
    rand_x = np.random.random(100)
    rand_y = np.random.random(100)
    c = np.arange(25, dtype='float32').reshape((5, 5))

    fig, axes = plt.subplots(3, 4)
    norm = mpl.colors.Normalize(4, 20)
    cl = mpl.colorizer.Colorizer(norm=norm, cmap='RdBu')

    match_str = "The `colorizer` keyword cannot be used simultaneously"
    kwrds = [{'vmin': 0}, {'vmax': 0}, {'norm': 'log'}, {'cmap': 'viridis'}]
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[0, 0].scatter(c, c, c=c, colorizer=cl, **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[0, 0].scatter(c, c, c=c, colorizer=cl, **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[0, 1].hexbin(rand_x, rand_y, colorizer=cl, gridsize=(2, 2), **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[0, 2].imshow(c, colorizer=cl, **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[0, 3].pcolor(c, colorizer=cl, **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[1, 0].pcolormesh(c, colorizer=cl, **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[1, 1].pcolorfast(c, colorizer=cl, **kwrd)  # style = image
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[1, 2].pcolorfast((0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 5, 6),  c,
                                  colorizer=cl, **kwrd)  # style = pcolorimage
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[1, 3].pcolorfast(c.T, c, c[:4, :4], colorizer=cl, **kwrd)  # quadmesh
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[2, 0].contour(c, colorizer=cl, **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[2, 1].contourf(c, colorizer=cl, **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[2, 2].tricontour(c.T.ravel(), c.ravel(), c.ravel(), colorizer=cl,
                                  **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            axes[2, 3].tricontourf(c.T.ravel(), c.ravel(), c.ravel(), colorizer=cl,
                                   **kwrd)
    for kwrd in kwrds:
        with pytest.raises(ValueError, match=match_str):
            fig.figimage(c, colorizer=cl, **kwrd)

