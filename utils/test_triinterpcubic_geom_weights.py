
def test_triinterpcubic_geom_weights():
    # Tests to check computation of weights for _DOF_estimator_geom:
    # The weight sum per triangle can be 1. (in case all angles < 90 degrees)
    # or (2*w_i) where w_i = 1-alpha_i/np.pi is the weight of apex i; alpha_i
    # is the apex angle > 90 degrees.
    (ax, ay) = (0., 1.687)
    x = np.array([ax, 0.5*ax, 0., 1.])
    y = np.array([ay, -ay, 0., 0.])
    z = np.zeros(4, dtype=np.float64)
    triangles = [[0, 2, 3], [1, 3, 2]]
    sum_w = np.zeros([4, 2])  # 4 possibilities; 2 triangles
    for theta in np.linspace(0., 2*np.pi, 14):  # rotating the figure...
        x_rot = np.cos(theta)*x + np.sin(theta)*y
        y_rot = -np.sin(theta)*x + np.cos(theta)*y
        triang = mtri.Triangulation(x_rot, y_rot, triangles)
        cubic_geom = mtri.CubicTriInterpolator(triang, z, kind='geom')
        dof_estimator = mtri._triinterpolate._DOF_estimator_geom(cubic_geom)
        weights = dof_estimator.compute_geom_weights()
        # Testing for the 4 possibilities...
        sum_w[0, :] = np.sum(weights, 1) - 1
        for itri in range(3):
            sum_w[itri+1, :] = np.sum(weights, 1) - 2*weights[:, itri]
        assert_array_almost_equal(np.min(np.abs(sum_w), axis=0),
                                  np.array([0., 0.], dtype=np.float64))

