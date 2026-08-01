
def test_poly_marker(fig_test, fig_ref):
    ax_test = fig_test.add_subplot()
    ax_ref = fig_ref.add_subplot()

    # Note, some reference sizes must be different because they have unit
    # *length*, while polygon markers are inscribed in a circle of unit
    # *radius*. This introduces a factor of np.sqrt(2), but since size is
    # squared, that becomes 2.
    size = 20**2

    # Squares
    ax_test.scatter([0], [0], marker=(4, 0, 45), s=size)
    ax_ref.scatter([0], [0], marker='s', s=size/2)

    # Diamonds, with and without rotation argument
    ax_test.scatter([1], [1], marker=(4, 0), s=size)
    ax_ref.scatter([1], [1], marker=UnsnappedMarkerStyle('D'), s=size/2)
    ax_test.scatter([1], [1.5], marker=(4, 0, 0), s=size)
    ax_ref.scatter([1], [1.5], marker=UnsnappedMarkerStyle('D'), s=size/2)

    # Pentagon, with and without rotation argument
    ax_test.scatter([2], [2], marker=(5, 0), s=size)
    ax_ref.scatter([2], [2], marker=UnsnappedMarkerStyle('p'), s=size)
    ax_test.scatter([2], [2.5], marker=(5, 0, 0), s=size)
    ax_ref.scatter([2], [2.5], marker=UnsnappedMarkerStyle('p'), s=size)

    # Hexagon, with and without rotation argument
    ax_test.scatter([3], [3], marker=(6, 0), s=size)
    ax_ref.scatter([3], [3], marker='h', s=size)
    ax_test.scatter([3], [3.5], marker=(6, 0, 0), s=size)
    ax_ref.scatter([3], [3.5], marker='h', s=size)

    # Rotated hexagon
    ax_test.scatter([4], [4], marker=(6, 0, 30), s=size)
    ax_ref.scatter([4], [4], marker='H', s=size)

    # Octagons
    ax_test.scatter([5], [5], marker=(8, 0, 22.5), s=size)
    ax_ref.scatter([5], [5], marker=UnsnappedMarkerStyle('8'), s=size)

    ax_test.set(xlim=(-0.5, 5.5), ylim=(-0.5, 5.5))
    ax_ref.set(xlim=(-0.5, 5.5), ylim=(-0.5, 5.5))

