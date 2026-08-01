
def test_text3d_modification(fig_ref, fig_test):
    # Modifying the Text position after the fact should work the same as
    # setting it directly.
    zdirs = (None, 'x', 'y', 'z', (1, 1, 0), (1, 1, 1))
    xs = (2, 6, 4, 9, 7, 2)
    ys = (6, 4, 8, 7, 2, 2)
    zs = (4, 2, 5, 6, 1, 7)

    ax_test = fig_test.add_subplot(projection='3d')
    ax_test.set_xlim3d(0, 10)
    ax_test.set_ylim3d(0, 10)
    ax_test.set_zlim3d(0, 10)
    for zdir, x, y, z in zip(zdirs, xs, ys, zs):
        t = ax_test.text(0, 0, 0, f'({x}, {y}, {z}), dir={zdir}')
        t.set_position_3d((x, y, z), zdir=zdir)

    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.set_xlim3d(0, 10)
    ax_ref.set_ylim3d(0, 10)
    ax_ref.set_zlim3d(0, 10)
    for zdir, x, y, z in zip(zdirs, xs, ys, zs):
        ax_ref.text(x, y, z, f'({x}, {y}, {z}), dir={zdir}', zdir=zdir)

