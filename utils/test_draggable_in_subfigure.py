
def test_draggable_in_subfigure():
    fig = plt.figure()
    # Put annotation at lower left corner to make it easily pickable below.
    ann = fig.subfigures().add_axes((0, 0, 1, 1)).annotate("foo", (0, 0))
    ann.draggable(True)
    fig.canvas.draw()  # Texts are non-pickable until the first draw.
    MouseEvent("button_press_event", fig.canvas, 1, 1)._process()
    assert ann._draggable.got_artist
    # Stop dragging the annotation.
    MouseEvent("button_release_event", fig.canvas, 1, 1)._process()
    assert not ann._draggable.got_artist
    # A scroll event should not initiate a drag.
    MouseEvent("scroll_event", fig.canvas, 1, 1)._process()
    assert not ann._draggable.got_artist
    # An event outside the annotation should not initiate a drag.
    bbox = ann.get_window_extent()
    MouseEvent("button_press_event", fig.canvas, bbox.x1+2, bbox.y1+2)._process()
    assert not ann._draggable.got_artist

