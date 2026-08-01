
def test_image_grid_each_left_label_mode_all():
    imdata = np.arange(100).reshape((10, 10))

    fig = plt.figure(1, (3, 3))
    grid = ImageGrid(fig, (1, 1, 1), nrows_ncols=(3, 2), axes_pad=(0.5, 0.3),
                     cbar_mode="each", cbar_location="left", cbar_size="15%",
                     label_mode="all")
    # 3-tuple rect => SubplotDivider
    assert isinstance(grid.get_divider(), SubplotDivider)
    assert grid.get_axes_pad() == (0.5, 0.3)
    assert grid.get_aspect()  # True by default for ImageGrid
    for ax, cax in zip(grid, grid.cbar_axes):
        im = ax.imshow(imdata, interpolation='none')
        cax.colorbar(im)

