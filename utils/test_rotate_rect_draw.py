
def test_rotate_rect_draw(fig_test, fig_ref):
    ax_test = fig_test.add_subplot()
    ax_ref = fig_ref.add_subplot()

    loc = (0, 0)
    width, height = (1, 1)
    angle = 30
    rect_ref = Rectangle(loc, width, height, angle=angle)
    ax_ref.add_patch(rect_ref)
    assert rect_ref.get_angle() == angle

    # Check that when the angle is updated after adding to an Axes, that the
    # patch is marked stale and redrawn in the correct location
    rect_test = Rectangle(loc, width, height)
    assert rect_test.get_angle() == 0
    ax_test.add_patch(rect_test)
    rect_test.set_angle(angle)
    assert rect_test.get_angle() == angle

