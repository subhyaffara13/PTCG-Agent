
def _generate_spherical_points(ndim=3, n_pts=2):
    # generate uniform points on sphere
    # see: https://stackoverflow.com/a/23785326
    # tentatively extended to arbitrary dims
    # for 0-sphere it will always produce antipodes
    np.random.seed(123)
    points = np.random.normal(size=(n_pts, ndim))
    points /= np.linalg.norm(points, axis=1)[:, np.newaxis]
    return points[0], points[1]

