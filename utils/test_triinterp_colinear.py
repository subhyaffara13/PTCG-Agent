
def test_triinterp_colinear():
    # Tests interpolating inside a triangulation with horizontal colinear
    # points (refer also to the tests :func:`test_trifinder` ).
    #
    # These are not valid triangulations, but we try to deal with the
    # simplest violations (i. e. those handled by default TriFinder).
    #
    # Note that the LinearTriInterpolator and the CubicTriInterpolator with
    # kind='min_E' or 'geom' still pass a linear patch test.
    # We also test interpolation inside a flat triangle, by forcing
    # *tri_index* in a call to :meth:`_interpolate_multikeys`.

    # If +ve, triangulation is OK, if -ve triangulation invalid,
    # if zero have colinear points but should pass tests anyway.
    delta = 0.

    x0 = np.array([1.5, 0,  1,  2, 3, 1.5,   1.5])
    y0 = np.array([-1,  0,  0,  0, 0, delta, 1])

    # We test different affine transformations of the initial figure; to
    # avoid issues related to round-off errors we only use integer
    # coefficients (otherwise the Triangulation might become invalid even with
    # delta == 0).
    transformations = [[1, 0], [0, 1], [1, 1], [1, 2], [-2, -1], [-2, 1]]
    for transformation in transformations:
        x_rot = transformation[0]*x0 + transformation[1]*y0
        y_rot = -transformation[1]*x0 + transformation[0]*y0
        (x, y) = (x_rot, y_rot)
        z = 1.23*x - 4.79*y
        triangles = [[0, 2, 1], [0, 3, 2], [0, 4, 3], [1, 2, 5], [2, 3, 5],
                     [3, 4, 5], [1, 5, 6], [4, 6, 5]]
        triang = mtri.Triangulation(x, y, triangles)
        xs = np.linspace(np.min(triang.x), np.max(triang.x), 20)
        ys = np.linspace(np.min(triang.y), np.max(triang.y), 20)
        xs, ys = np.meshgrid(xs, ys)
        xs = xs.ravel()
        ys = ys.ravel()
        mask_out = (triang.get_trifinder()(xs, ys) == -1)
        zs_target = np.ma.array(1.23*xs - 4.79*ys, mask=mask_out)

        linear_interp = mtri.LinearTriInterpolator(triang, z)
        cubic_min_E = mtri.CubicTriInterpolator(triang, z)
        cubic_geom = mtri.CubicTriInterpolator(triang, z, kind='geom')

        for interp in (linear_interp, cubic_min_E, cubic_geom):
            zs = interp(xs, ys)
            assert_array_almost_equal(zs_target, zs)

        # Testing interpolation inside the flat triangle number 4: [2, 3, 5]
        # by imposing *tri_index* in a call to :meth:`_interpolate_multikeys`
        itri = 4
        pt1 = triang.triangles[itri, 0]
        pt2 = triang.triangles[itri, 1]
        xs = np.linspace(triang.x[pt1], triang.x[pt2], 10)
        ys = np.linspace(triang.y[pt1], triang.y[pt2], 10)
        zs_target = 1.23*xs - 4.79*ys
        for interp in (linear_interp, cubic_min_E, cubic_geom):
            zs, = interp._interpolate_multikeys(
                xs, ys, tri_index=itri*np.ones(10, dtype=np.int32))
            assert_array_almost_equal(zs_target, zs)

