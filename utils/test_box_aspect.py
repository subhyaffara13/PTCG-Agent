
def test_box_aspect():
    # Test if axes with box_aspect=1 has same dimensions
    # as axes with aspect equal and adjustable="box"

    fig1, ax1 = plt.subplots()
    axtwin = ax1.twinx()
    axtwin.plot([12, 344])

    ax1.set_box_aspect(1)
    assert ax1.get_box_aspect() == 1.0

    fig2, ax2 = plt.subplots()
    ax2.margins(0)
    ax2.plot([0, 2], [6, 8])
    ax2.set_aspect("equal", adjustable="box")

    fig1.canvas.draw()
    fig2.canvas.draw()

    bb1 = ax1.get_position()
    bbt = axtwin.get_position()
    bb2 = ax2.get_position()

    assert_array_equal(bb1.extents, bb2.extents)
    assert_array_equal(bbt.extents, bb2.extents)

