
def test_compressed_supylabel_colorbar():
    """
    Test that horizontal colorbars align with axes
    in compressed layout with supylabel.
    """
    arr = np.arange(100).reshape((10, 10))
    fig, axs = plt.subplots(nrows=2, figsize=(3, 4), layout='compressed')

    im0 = axs[0].imshow(arr)
    im1 = axs[1].imshow(arr)

    cb0 = plt.colorbar(im0, ax=axs[0], orientation='horizontal')
    cb1 = plt.colorbar(im1, ax=axs[1], orientation='horizontal')

    fig.supylabel('Title')

    # Verify colorbar widths match axes widths
    # After layout, colorbar should have same width as parent axes
    fig.canvas.draw()

    for ax, cb in zip(axs, [cb0, cb1]):
        ax_pos = ax.get_position()
        cb_pos = cb.ax.get_position()

        # Check that colorbar width matches axes width (within tolerance)
        # Note: We check the actual rendered positions, not the bbox
        assert abs(cb_pos.width - ax_pos.width) < 0.01, \
            f"Colorbar width {cb_pos.width} doesn't match axes width {ax_pos.width}"

        # Also verify horizontal alignment (x0 and x1 should match)
        assert abs(cb_pos.x0 - ax_pos.x0) < 0.01, \
            f"Colorbar x0 {cb_pos.x0} doesn't match axes x0 {ax_pos.x0}"
        assert abs(cb_pos.x1 - ax_pos.x1) < 0.01, \
            f"Colorbar x1 {cb_pos.x1} doesn't match axes x1 {ax_pos.x1}"

