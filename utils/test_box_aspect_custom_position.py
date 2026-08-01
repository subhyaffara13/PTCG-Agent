
def test_box_aspect_custom_position():
    # Test if axes with custom position and box_aspect
    # behaves the same independent of the order of setting those.

    fig1, ax1 = plt.subplots()
    ax1.set_position([0.1, 0.1, 0.9, 0.2])
    fig1.canvas.draw()
    ax1.set_box_aspect(1.)

    fig2, ax2 = plt.subplots()
    ax2.set_box_aspect(1.)
    fig2.canvas.draw()
    ax2.set_position([0.1, 0.1, 0.9, 0.2])

    fig1.canvas.draw()
    fig2.canvas.draw()

    bb1 = ax1.get_position()
    bb2 = ax2.get_position()

    assert_array_equal(bb1.extents, bb2.extents)

