
def test_rectangle_rotate(ax, selector_class):
    tool = selector_class(ax, interactive=True)
    # Draw rectangle
    click_and_drag(tool, start=(100, 100), end=(130, 140))
    assert tool.extents == (100, 130, 100, 140)
    assert len(tool._state) == 0

    # Rotate anticlockwise using top-right corner
    KeyEvent("key_press_event", ax.figure.canvas, "r")._process()
    assert tool._state == {'rotate'}
    assert len(tool._state) == 1
    click_and_drag(tool, start=(130, 140), end=(120, 145))
    KeyEvent("key_press_event", ax.figure.canvas, "r")._process()
    assert len(tool._state) == 0
    # Extents shouldn't change (as shape of rectangle hasn't changed)
    assert tool.extents == (100, 130, 100, 140)
    assert_allclose(tool.rotation, 25.56, atol=0.01)
    tool.rotation = 45
    assert tool.rotation == 45
    # Corners should move
    assert_allclose(tool.corners,
                    np.array([[118.53, 139.75, 111.46, 90.25],
                              [95.25, 116.46, 144.75, 123.54]]), atol=0.01)

    # Scale using top-right corner
    click_and_drag(tool, start=(110, 145), end=(110, 160))
    assert_allclose(tool.extents, (100, 139.75, 100, 151.82), atol=0.01)

    if selector_class == widgets.RectangleSelector:
        with pytest.raises(ValueError):
            tool._selection_artist.rotation_point = 'unvalid_value'

