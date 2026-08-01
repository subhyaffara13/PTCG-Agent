
def test_axis_get_tightbbox_includes_offset_text():
    # Test that axis.get_tightbbox includes the offset_text
    # Regression test for issue #30744
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create data with high precision values that trigger offset text
    Z = np.array([[0.1, 0.100000001], [0.100000000001, 0.100000000]])
    ny, nx = Z.shape
    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y)

    ax.plot_surface(X, Y, Z)

    # Force a draw to ensure offset text is created and positioned
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    # Get the z-axis (which should have the offset text)
    zaxis = ax.zaxis

    # Check that offset text is visible and has content
    # The offset text may not be visible on all backends/configurations,
    # so we only test the inclusion when it's actually present
    if (zaxis.offsetText.get_visible() and
        zaxis.offsetText.get_text()):
        offset_bbox = zaxis.offsetText.get_window_extent(renderer)

        # Get the tight bbox - this should include the offset text
        bbox = zaxis.get_tightbbox(renderer)
        assert bbox is not None
        assert offset_bbox is not None

        # The tight bbox should fully contain the offset text bbox
        # Check that offset_bbox is within bbox bounds (with small tolerance for
        # floating point errors)
        assert bbox.x0 <= offset_bbox.x0 + 1e-6, \
            f"bbox.x0 ({bbox.x0}) should be <= offset_bbox.x0 ({offset_bbox.x0})"
        assert bbox.y0 <= offset_bbox.y0 + 1e-6, \
            f"bbox.y0 ({bbox.y0}) should be <= offset_bbox.y0 ({offset_bbox.y0})"
        assert bbox.x1 >= offset_bbox.x1 - 1e-6, \
            f"bbox.x1 ({bbox.x1}) should be >= offset_bbox.x1 ({offset_bbox.x1})"
        assert bbox.y1 >= offset_bbox.y1 - 1e-6, \
            f"bbox.y1 ({bbox.y1}) should be >= offset_bbox.y1 ({offset_bbox.y1})"

