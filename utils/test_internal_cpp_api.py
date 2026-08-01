
def test_internal_cpp_api() -> None:
    # Following github issue 8197.
    from matplotlib import _tri  # noqa: F401, ensure lazy-loaded module *is* loaded.

    # C++ Triangulation.
    with pytest.raises(
            TypeError,
            match=r'__init__\(\): incompatible constructor arguments.'):
        mpl._tri.Triangulation()  # type: ignore[call-arg]

    with pytest.raises(
            ValueError, match=r'x and y must be 1D arrays of the same length'):
        mpl._tri.Triangulation(np.array([]), np.array([1]), np.array([[]]), (), (), (),
                               False)

    x = np.array([0, 1, 1], dtype=np.float64)
    y = np.array([0, 0, 1], dtype=np.float64)
    with pytest.raises(
            ValueError,
            match=r'triangles must be a 2D array of shape \(\?,3\)'):
        mpl._tri.Triangulation(x, y, np.array([[0, 1]]), (), (), (), False)

    tris = np.array([[0, 1, 2]], dtype=np.int_)
    with pytest.raises(
            ValueError,
            match=r'mask must be a 1D array with the same length as the '
                  r'triangles array'):
        mpl._tri.Triangulation(x, y, tris, np.array([0, 1]), (), (), False)

    with pytest.raises(
            ValueError, match=r'edges must be a 2D array with shape \(\?,2\)'):
        mpl._tri.Triangulation(x, y, tris, (), np.array([[1]]), (), False)

    with pytest.raises(
            ValueError,
            match=r'neighbors must be a 2D array with the same shape as the '
                  r'triangles array'):
        mpl._tri.Triangulation(x, y, tris, (), (), np.array([[-1]]), False)

    triang = mpl._tri.Triangulation(x, y, tris, (), (), (), False)

    with pytest.raises(
            ValueError,
            match=r'z must be a 1D array with the same length as the '
                  r'triangulation x and y arrays'):
        triang.calculate_plane_coefficients([])

    for mask in ([0, 1], None):
        with pytest.raises(
                ValueError,
                match=r'mask must be a 1D array with the same length as the '
                      r'triangles array'):
            triang.set_mask(mask)  # type: ignore[arg-type]

    triang.set_mask(np.array([True]))
    assert_array_equal(triang.get_edges(), np.empty((0, 2)))

    triang.set_mask(())  # Equivalent to Python Triangulation mask=None
    assert_array_equal(triang.get_edges(), [[1, 0], [2, 0], [2, 1]])

    # C++ TriContourGenerator.
    with pytest.raises(
            TypeError,
            match=r'__init__\(\): incompatible constructor arguments.'):
        mpl._tri.TriContourGenerator()  # type: ignore[call-arg]

    with pytest.raises(
            ValueError,
            match=r'z must be a 1D array with the same length as the x and y arrays'):
        mpl._tri.TriContourGenerator(triang, np.array([1]))

    z = np.array([0, 1, 2])
    tcg = mpl._tri.TriContourGenerator(triang, z)

    with pytest.raises(
            ValueError, match=r'filled contour levels must be increasing'):
        tcg.create_filled_contour(1, 0)

    # C++ TrapezoidMapTriFinder.
    with pytest.raises(
            TypeError,
            match=r'__init__\(\): incompatible constructor arguments.'):
        mpl._tri.TrapezoidMapTriFinder()  # type: ignore[call-arg]

    trifinder = mpl._tri.TrapezoidMapTriFinder(triang)

    with pytest.raises(
            ValueError, match=r'x and y must be array-like with same shape'):
        trifinder.find_many(np.array([0]), np.array([0, 1]))

