
def test_asterisk_marker(fig_test, fig_ref, request):
    ax_test = fig_test.add_subplot()
    ax_ref = fig_ref.add_subplot()

    # Note, some reference sizes must be different because they have unit
    # *length*, while asterisk markers are inscribed in a circle of unit
    # *radius*. This introduces a factor of np.sqrt(2), but since size is
    # squared, that becomes 2.
    size = 20**2

    def draw_ref_marker(y, style, size):
        # As noted above, every line is doubled. Due to antialiasing, these
        # doubled lines make a slight difference in the .png results.
        ax_ref.scatter([y], [y], marker=UnsnappedMarkerStyle(style), s=size)
        if request.getfixturevalue('ext') == 'png':
            ax_ref.scatter([y], [y], marker=UnsnappedMarkerStyle(style),
                           s=size)

    # Plus
    ax_test.scatter([0], [0], marker=(4, 2), s=size)
    draw_ref_marker(0, '+', size)
    ax_test.scatter([0.5], [0.5], marker=(4, 2, 0), s=size)
    draw_ref_marker(0.5, '+', size)

    # Cross
    ax_test.scatter([1], [1], marker=(4, 2, 45), s=size)
    draw_ref_marker(1, 'x', size/2)

    ax_test.set(xlim=(-0.5, 1.5), ylim=(-0.5, 1.5))
    ax_ref.set(xlim=(-0.5, 1.5), ylim=(-0.5, 1.5))

