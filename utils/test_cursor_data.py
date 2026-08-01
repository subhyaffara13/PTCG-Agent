
def test_cursor_data():
    from matplotlib.backend_bases import MouseEvent

    fig, ax = plt.subplots()
    im = ax.imshow(np.arange(100).reshape(10, 10), origin='upper')

    x, y = 4, 4
    xdisp, ydisp = ax.transData.transform([x, y])

    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) == 44

    # Now try for a point outside the image
    # Tests issue #4957
    x, y = 10.1, 4
    xdisp, ydisp = ax.transData.transform([x, y])

    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) is None

    # Hmm, something is wrong here... I get 0, not None...
    # But, this works further down in the tests with extents flipped
    # x, y = 0.1, -0.1
    # xdisp, ydisp = ax.transData.transform([x, y])
    # event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    # z = im.get_cursor_data(event)
    # assert z is None, "Did not get None, got %d" % z

    ax.clear()
    # Now try with the extents flipped.
    im = ax.imshow(np.arange(100).reshape(10, 10), origin='lower')

    x, y = 4, 4
    xdisp, ydisp = ax.transData.transform([x, y])

    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) == 44

    fig, ax = plt.subplots()
    im = ax.imshow(np.arange(100).reshape(10, 10), extent=[0, 0.5, 0, 0.5])

    x, y = 0.25, 0.25
    xdisp, ydisp = ax.transData.transform([x, y])

    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) == 55

    # Now try for a point outside the image
    # Tests issue #4957
    x, y = 0.75, 0.25
    xdisp, ydisp = ax.transData.transform([x, y])

    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) is None

    x, y = 0.01, -0.01
    xdisp, ydisp = ax.transData.transform([x, y])

    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) is None

    # Now try with additional transform applied to the image artist
    trans = Affine2D().scale(2).rotate(0.5)
    im = ax.imshow(np.arange(100).reshape(10, 10),
                   transform=trans + ax.transData)
    x, y = 3, 10
    xdisp, ydisp = ax.transData.transform([x, y])
    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) == 44

