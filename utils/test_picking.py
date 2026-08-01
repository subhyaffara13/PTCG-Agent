
def test_picking():
    fig, ax = plt.subplots()
    col = ax.scatter([0], [0], [1000], picker=True)
    fig.savefig(io.BytesIO(), dpi=fig.dpi)
    mouse_event = SimpleNamespace(x=325, y=240)
    found, indices = col.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [0])


def test_picking():
    fig, ax = plt.subplots()
    mouse_event = SimpleNamespace(x=fig.bbox.width // 2,
                                  y=fig.bbox.height // 2 + 15)

    # Default pickradius is 5, so event should not pick this line.
    l0, = ax.plot([0, 1], [0, 1], picker=True)
    found, indices = l0.contains(mouse_event)
    assert not found

    # But with a larger pickradius, this should be picked.
    l1, = ax.plot([0, 1], [0, 1], picker=True, pickradius=20)
    found, indices = l1.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [0])

    # And if we modify the pickradius after creation, it should work as well.
    l2, = ax.plot([0, 1], [0, 1], picker=True)
    found, indices = l2.contains(mouse_event)
    assert not found
    l2.set_pickradius(20)
    found, indices = l2.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [0])


def test_picking(child_type, boxcoords):
    # These all take up approximately the same area.
    if child_type == 'draw':
        picking_child = DrawingArea(5, 5)
        picking_child.add_artist(mpatches.Rectangle((0, 0), 5, 5, linewidth=0))
    elif child_type == 'image':
        im = np.ones((5, 5))
        im[2, 2] = 0
        picking_child = OffsetImage(im)
    elif child_type == 'text':
        picking_child = TextArea('\N{Black Square}', textprops={'fontsize': 5})
    else:
        assert False, f'Unknown picking child type {child_type}'

    fig, ax = plt.subplots()
    ab = AnnotationBbox(picking_child, (0.5, 0.5), boxcoords=boxcoords)
    ab.set_picker(True)
    ax.add_artist(ab)

    calls = []
    fig.canvas.mpl_connect('pick_event', lambda event: calls.append(event))

    # Annotation should be picked by an event occurring at its center.
    if boxcoords == 'axes points':
        x, y = ax.transAxes.transform_point((0, 0))
        x += 0.5 * fig.dpi / 72
        y += 0.5 * fig.dpi / 72
    elif boxcoords == 'axes pixels':
        x, y = ax.transAxes.transform_point((0, 0))
        x += 0.5
        y += 0.5
    else:
        x, y = ax.transAxes.transform_point((0.5, 0.5))
    fig.canvas.draw()
    calls.clear()
    MouseEvent(
        "button_press_event", fig.canvas, x, y, MouseButton.LEFT)._process()
    assert len(calls) == 1 and calls[0].artist == ab

    # Annotation should *not* be picked by an event at its original center
    # point when the limits have changed enough to hide the *xy* point.
    ax.set_xlim(-1, 0)
    ax.set_ylim(-1, 0)
    fig.canvas.draw()
    calls.clear()
    MouseEvent(
        "button_press_event", fig.canvas, x, y, MouseButton.LEFT)._process()
    assert len(calls) == 0

