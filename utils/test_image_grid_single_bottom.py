
def test_image_grid_single_bottom():
    imdata = np.arange(100).reshape((10, 10))

    fig = plt.figure(1, (2.5, 1.5))
    grid = ImageGrid(fig, (0, 0, 1, 1), nrows_ncols=(1, 3),
                     axes_pad=(0.2, 0.15), cbar_mode="single", cbar_pad=0.3,
                     cbar_location="bottom", cbar_size="10%", label_mode="1")
    # 4-tuple rect => Divider, isinstance will give True for SubplotDivider
    assert type(grid.get_divider()) is Divider
    for i in range(3):
        im = grid[i].imshow(imdata, interpolation='none')
    grid.cbar_axes[0].colorbar(im)

