
def test_ellipse(ax):
    """For ellipse, test out the key modifiers"""
    tool = widgets.EllipseSelector(ax, grab_range=10, interactive=True)
    tool.extents = (100, 150, 100, 150)

    # drag the rectangle
    click_and_drag(tool, start=(125, 125), end=(145, 145))
    assert tool.extents == (120, 170, 120, 170)

    # create from center
    click_and_drag(tool, start=(100, 100), end=(125, 125), key='control')
    assert tool.extents == (75, 125, 75, 125)

    # create a square
    click_and_drag(tool, start=(10, 10), end=(35, 30), key='shift')
    extents = [int(e) for e in tool.extents]
    assert extents == [10, 35, 10, 35]

    # create a square from center
    click_and_drag(tool, start=(100, 100), end=(125, 130), key='ctrl+shift')
    extents = [int(e) for e in tool.extents]
    assert extents == [70, 130, 70, 130]

    assert tool.geometry.shape == (2, 73)
    assert_allclose(tool.geometry[:, 0], [70., 100])

