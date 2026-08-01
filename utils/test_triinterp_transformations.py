
def test_triinterp_transformations():
    # 1) Testing that the interpolation scheme is invariant by rotation of the
    # whole figure.
    # Note: This test is non-trivial for a CubicTriInterpolator with
    # kind='min_E'. It does fail for a non-isotropic stiffness matrix E of
    # :class:`_ReducedHCT_Element` (tested with E=np.diag([1., 1., 1.])), and
    # provides a good test for :meth:`get_Kff_and_Ff`of the same class.
    #
    # 2) Also testing that the interpolation scheme is invariant by expansion
    # of the whole figure along one axis.
    n_angles = 20
    n_radii = 10
    min_radius = 0.15

    def z(x, y):
        r1 = np.hypot(0.5 - x, 0.5 - y)
        theta1 = np.arctan2(0.5 - x, 0.5 - y)
        r2 = np.hypot(-x - 0.2, -y - 0.2)
        theta2 = np.arctan2(-x - 0.2, -y - 0.2)
        z = -(2*(np.exp((r1/10)**2)-1)*30. * np.cos(7.*theta1) +
              (np.exp((r2/10)**2)-1)*30. * np.cos(11.*theta2) +
              0.7*(x**2 + y**2))
        return (np.max(z)-z)/(np.max(z)-np.min(z))

    # First create the x and y coordinates of the points.
    radii = np.linspace(min_radius, 0.95, n_radii)
    angles = np.linspace(0 + n_angles, 2*np.pi + n_angles,
                         n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    angles[:, 1::2] += np.pi/n_angles
    x0 = (radii*np.cos(angles)).flatten()
    y0 = (radii*np.sin(angles)).flatten()
    triang0 = mtri.Triangulation(x0, y0)  # Delaunay triangulation
    z0 = z(x0, y0)

    # Then create the test points
    xs0 = np.linspace(-1., 1., 23)
    ys0 = np.linspace(-1., 1., 23)
    xs0, ys0 = np.meshgrid(xs0, ys0)
    xs0 = xs0.ravel()
    ys0 = ys0.ravel()

    interp_z0 = {}
    for i_angle in range(2):
        # Rotating everything
        theta = 2*np.pi / n_angles * i_angle
        x = np.cos(theta)*x0 + np.sin(theta)*y0
        y = -np.sin(theta)*x0 + np.cos(theta)*y0
        xs = np.cos(theta)*xs0 + np.sin(theta)*ys0
        ys = -np.sin(theta)*xs0 + np.cos(theta)*ys0
        triang = mtri.Triangulation(x, y, triang0.triangles)
        linear_interp = mtri.LinearTriInterpolator(triang, z0)
        cubic_min_E = mtri.CubicTriInterpolator(triang, z0)
        cubic_geom = mtri.CubicTriInterpolator(triang, z0, kind='geom')
        dic_interp = {'lin': linear_interp,
                      'min_E': cubic_min_E,
                      'geom': cubic_geom}
        # Testing that the interpolation is invariant by rotation...
        for interp_key in ['lin', 'min_E', 'geom']:
            interp = dic_interp[interp_key]
            if i_angle == 0:
                interp_z0[interp_key] = interp(xs0, ys0)  # storage
            else:
                interpz = interp(xs, ys)
                matest.assert_array_almost_equal(interpz,
                                                 interp_z0[interp_key])

    scale_factor = 987654.3210
    for scaled_axis in ('x', 'y'):
        # Scaling everything (expansion along scaled_axis)
        if scaled_axis == 'x':
            x = scale_factor * x0
            y = y0
            xs = scale_factor * xs0
            ys = ys0
        else:
            x = x0
            y = scale_factor * y0
            xs = xs0
            ys = scale_factor * ys0
        triang = mtri.Triangulation(x, y, triang0.triangles)
        linear_interp = mtri.LinearTriInterpolator(triang, z0)
        cubic_min_E = mtri.CubicTriInterpolator(triang, z0)
        cubic_geom = mtri.CubicTriInterpolator(triang, z0, kind='geom')
        dic_interp = {'lin': linear_interp,
                      'min_E': cubic_min_E,
                      'geom': cubic_geom}
        # Test that the interpolation is invariant by expansion along 1 axis...
        for interp_key in ['lin', 'min_E', 'geom']:
            interpz = dic_interp[interp_key](xs, ys)
            matest.assert_array_almost_equal(interpz, interp_z0[interp_key])

