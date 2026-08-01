
def test_rectangle_drag(ax, drag_from_anywhere, new_center):
    tool = widgets.RectangleSelector(ax, interactive=True,
                                     drag_from_anywhere=drag_from_anywhere)
    # Create rectangle
    click_and_drag(tool, start=(10, 10), end=(90, 120))
    assert tool.center == (50, 65)
    # Drag inside rectangle, but away from centre handle
    #
    # If drag_from_anywhere == True, this will move the rectangle by (10, 10),
    # giving it a new center of (60, 75)
    #
    # If drag_from_anywhere == False, this will create a new rectangle with
    # center (30, 20)
    click_and_drag(tool, start=(25, 15), end=(35, 25))
    assert tool.center == new_center
    # Check that in both cases, dragging outside the rectangle draws a new
    # rectangle
    click_and_drag(tool, start=(175, 185), end=(185, 195))
    assert tool.center == (180, 190)

