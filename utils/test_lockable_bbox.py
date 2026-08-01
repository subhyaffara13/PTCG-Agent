
def test_lockable_bbox(locked_element):
    other_elements = ['x0', 'y0', 'x1', 'y1']
    other_elements.remove(locked_element)

    orig = mtransforms.Bbox.unit()
    locked = mtransforms.LockableBbox(orig, **{locked_element: 2})

    # LockableBbox should keep its locked element as specified in __init__.
    assert getattr(locked, locked_element) == 2
    assert getattr(locked, 'locked_' + locked_element) == 2
    for elem in other_elements:
        assert getattr(locked, elem) == getattr(orig, elem)

    # Changing underlying Bbox should update everything but locked element.
    orig.set_points(orig.get_points() + 10)
    assert getattr(locked, locked_element) == 2
    assert getattr(locked, 'locked_' + locked_element) == 2
    for elem in other_elements:
        assert getattr(locked, elem) == getattr(orig, elem)

    # Unlocking element should revert values back to the underlying Bbox.
    setattr(locked, 'locked_' + locked_element, None)
    assert getattr(locked, 'locked_' + locked_element) is None
    assert np.all(orig.get_points() == locked.get_points())

    # Relocking an element should change its value, but not others.
    setattr(locked, 'locked_' + locked_element, 3)
    assert getattr(locked, locked_element) == 3
    assert getattr(locked, 'locked_' + locked_element) == 3
    for elem in other_elements:
        assert getattr(locked, elem) == getattr(orig, elem)

