
def test_rectangle_resize_square_center_aspect(ax, use_data_coordinates):
    ax.set_aspect(0.8)

    tool = widgets.RectangleSelector(ax, interactive=True,
                                     use_data_coordinates=use_data_coordinates)
    # Create rectangle
    click_and_drag(tool, start=(70, 65), end=(120, 115))
    assert tool.extents == (70.0, 120.0, 65.0, 115.0)
    tool.add_state('square')
    tool.add_state('center')

    if use_data_coordinates:
        # resize E handle
        extents = tool.extents
        xdata, ydata, width = extents[1], extents[3], extents[1] - extents[0]
        xdiff, ycenter = 10,  extents[2] + (extents[3] - extents[2]) / 2
        xdata_new, ydata_new = xdata + xdiff, ydata
        ychange = width / 2 + xdiff
        click_and_drag(tool, start=(xdata, ydata), end=(xdata_new, ydata_new))
        assert_allclose(tool.extents, [extents[0] - xdiff, xdata_new,
                                       ycenter - ychange, ycenter + ychange])
    else:
        # resize E handle
        extents = tool.extents
        xdata, ydata = extents[1], extents[3]
        xdiff = 10
        xdata_new, ydata_new = xdata + xdiff, ydata
        ychange = xdiff * 1 / tool._aspect_ratio_correction
        click_and_drag(tool, start=(xdata, ydata), end=(xdata_new, ydata_new))
        assert_allclose(tool.extents, [extents[0] - xdiff, xdata_new,
                                       46.25, 133.75])

