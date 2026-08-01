
def test_triinterpcubic_C1_continuity():
    # Below the 4 tests which demonstrate C1 continuity of the
    # TriCubicInterpolator (testing the cubic shape functions on arbitrary
    # triangle):
    #
    # 1) Testing continuity of function & derivatives at corner for all 9
    #    shape functions. Testing also function values at same location.
    # 2) Testing C1 continuity along each edge (as gradient is polynomial of
    #    2nd order, it is sufficient to test at the middle).
    # 3) Testing C1 continuity at triangle barycenter (where the 3 subtriangles
    #    meet)
    # 4) Testing C1 continuity at median 1/3 points (midside between 2
    #    subtriangles)

    # Utility test function check_continuity
    def check_continuity(interpolator, loc, values=None):
        """
        Checks the continuity of interpolator (and its derivatives) near
        location loc. Can check the value at loc itself if *values* is
        provided.

        *interpolator* TriInterpolator
        *loc* location to test (x0, y0)
        *values* (optional) array [z0, dzx0, dzy0] to check the value at *loc*
        """
        n_star = 24       # Number of continuity points in a boundary of loc
        epsilon = 1.e-10  # Distance for loc boundary
        k = 100.          # Continuity coefficient
        (loc_x, loc_y) = loc
        star_x = loc_x + epsilon*np.cos(np.linspace(0., 2*np.pi, n_star))
        star_y = loc_y + epsilon*np.sin(np.linspace(0., 2*np.pi, n_star))
        z = interpolator([loc_x], [loc_y])[0]
        (dzx, dzy) = interpolator.gradient([loc_x], [loc_y])
        if values is not None:
            assert_array_almost_equal(z, values[0])
            assert_array_almost_equal(dzx[0], values[1])
            assert_array_almost_equal(dzy[0], values[2])
        diff_z = interpolator(star_x, star_y) - z
        (tab_dzx, tab_dzy) = interpolator.gradient(star_x, star_y)
        diff_dzx = tab_dzx - dzx
        diff_dzy = tab_dzy - dzy
        assert_array_less(diff_z, epsilon*k)
        assert_array_less(diff_dzx, epsilon*k)
        assert_array_less(diff_dzy, epsilon*k)

    # Drawing arbitrary triangle (a, b, c) inside a unit square.
    (ax, ay) = (0.2, 0.3)
    (bx, by) = (0.33367, 0.80755)
    (cx, cy) = (0.669, 0.4335)
    x = np.array([ax, bx, cx, 0., 1., 1., 0.])
    y = np.array([ay, by, cy, 0., 0., 1., 1.])
    triangles = np.array([[0, 1, 2], [3, 0, 4], [4, 0, 2], [4, 2, 5],
                          [1, 5, 2], [6, 5, 1], [6, 1, 0], [6, 0, 3]])
    triang = mtri.Triangulation(x, y, triangles)

    for idof in range(9):
        z = np.zeros(7, dtype=np.float64)
        dzx = np.zeros(7, dtype=np.float64)
        dzy = np.zeros(7, dtype=np.float64)
        values = np.zeros([3, 3], dtype=np.float64)
        case = idof//3
        values[case, idof % 3] = 1.0
        if case == 0:
            z[idof] = 1.0
        elif case == 1:
            dzx[idof % 3] = 1.0
        elif case == 2:
            dzy[idof % 3] = 1.0
        interp = mtri.CubicTriInterpolator(triang, z, kind='user',
                                           dz=(dzx, dzy))
        # Test 1) Checking values and continuity at nodes
        check_continuity(interp, (ax, ay), values[:, 0])
        check_continuity(interp, (bx, by), values[:, 1])
        check_continuity(interp, (cx, cy), values[:, 2])
        # Test 2) Checking continuity at midside nodes
        check_continuity(interp, ((ax+bx)*0.5, (ay+by)*0.5))
        check_continuity(interp, ((ax+cx)*0.5, (ay+cy)*0.5))
        check_continuity(interp, ((cx+bx)*0.5, (cy+by)*0.5))
        # Test 3) Checking continuity at barycenter
        check_continuity(interp, ((ax+bx+cx)/3., (ay+by+cy)/3.))
        # Test 4) Checking continuity at median 1/3-point
        check_continuity(interp, ((4.*ax+bx+cx)/6., (4.*ay+by+cy)/6.))
        check_continuity(interp, ((ax+4.*bx+cx)/6., (ay+4.*by+cy)/6.))
        check_continuity(interp, ((ax+bx+4.*cx)/6., (ay+by+4.*cy)/6.))

