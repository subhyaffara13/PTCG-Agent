
def test_rectangle_resize(ax):
    tool = widgets.RectangleSelector(ax, interactive=True)
    # Create rectangle
    click_and_drag(tool, start=(10, 10), end=(100, 120))
    assert tool.extents == (10.0, 100.0, 10.0, 120.0)

    # resize NE handle
    extents = tool.extents
    xdata, ydata = extents[1], extents[3]
    xdata_new, ydata_new = xdata + 10, ydata + 5
    click_and_drag(tool, start=(xdata, ydata), end=(xdata_new, ydata_new))
    assert tool.extents == (extents[0], xdata_new, extents[2], ydata_new)

    # resize E handle
    extents = tool.extents
    xdata, ydata = extents[1], extents[2] + (extents[3] - extents[2]) / 2
    xdata_new, ydata_new = xdata + 10, ydata
    click_and_drag(tool, start=(xdata, ydata), end=(xdata_new, ydata_new))
    assert tool.extents == (extents[0], xdata_new, extents[2], extents[3])

    # resize W handle
    extents = tool.extents
    xdata, ydata = extents[0], extents[2] + (extents[3] - extents[2]) / 2
    xdata_new, ydata_new = xdata + 15, ydata
    click_and_drag(tool, start=(xdata, ydata), end=(xdata_new, ydata_new))
    assert tool.extents == (xdata_new, extents[1], extents[2], extents[3])

    # resize SW handle
    extents = tool.extents
    xdata, ydata = extents[0], extents[2]
    xdata_new, ydata_new = xdata + 20, ydata + 25
    click_and_drag(tool, start=(xdata, ydata), end=(xdata_new, ydata_new))
    assert tool.extents == (xdata_new, extents[1], ydata_new, extents[3])

