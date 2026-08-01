
def test_compressed_suptitle_colorbar():
    """Test that colorbars align with axes in compressed layout with suptitle."""
    arr = np.arange(100).reshape((10, 10))
    fig, axs = plt.subplots(ncols=2, figsize=(4, 2), layout='compressed')

    im0 = axs[0].imshow(arr)
    im1 = axs[1].imshow(arr)

    cb0 = plt.colorbar(im0, ax=axs[0])
    cb1 = plt.colorbar(im1, ax=axs[1])

    fig.suptitle('Title')

    # Verify colorbar heights match axes heights
    # After layout, colorbar should have same height as parent axes
    fig.canvas.draw()

    for ax, cb in zip(axs, [cb0, cb1]):
        ax_pos = ax.get_position()
        cb_pos = cb.ax.get_position()

        # Check that colorbar height matches axes height (within tolerance)
        # Note: We check the actual rendered positions, not the bbox
        assert abs(cb_pos.height - ax_pos.height) < 0.01, \
            f"Colorbar height {cb_pos.height} doesn't match axes height {ax_pos.height}"

        # Also verify vertical alignment (y0 and y1 should match)
        assert abs(cb_pos.y0 - ax_pos.y0) < 0.01, \
            f"Colorbar y0 {cb_pos.y0} doesn't match axes y0 {ax_pos.y0}"
        assert abs(cb_pos.y1 - ax_pos.y1) < 0.01, \
            f"Colorbar y1 {cb_pos.y1} doesn't match axes y1 {ax_pos.y1}"

