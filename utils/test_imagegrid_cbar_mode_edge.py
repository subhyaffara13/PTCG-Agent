
def test_imagegrid_cbar_mode_edge():
    arr = np.arange(16).reshape((4, 4))

    fig = plt.figure(figsize=(18, 9))

    positions = (241, 242, 243, 244, 245, 246, 247, 248)
    directions = ['row']*4 + ['column']*4
    cbar_locations = ['left', 'right', 'top', 'bottom']*2

    for position, direction, location in zip(
            positions, directions, cbar_locations):
        grid = ImageGrid(fig, position,
                         nrows_ncols=(2, 2),
                         direction=direction,
                         cbar_location=location,
                         cbar_size='20%',
                         cbar_mode='edge')
        ax1, ax2, ax3, ax4 = grid

        ax1.imshow(arr, cmap='nipy_spectral')
        ax2.imshow(arr.T, cmap='hot')
        ax3.imshow(np.hypot(arr, arr.T), cmap='jet')
        ax4.imshow(np.arctan2(arr, arr.T), cmap='hsv')

        # In each row/column, the "first" colorbars must be overwritten by the
        # "second" ones.  To achieve this, clear out the axes first.
        for ax in grid:
            ax.cax.cla()
            cb = ax.cax.colorbar(ax.images[0])

