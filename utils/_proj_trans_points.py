
def _proj_trans_points(points, M):
    points = np.asanyarray(points)
    xs, ys, zs = points[:, 0], points[:, 1], points[:, 2]
    return proj_transform(xs, ys, zs, M)

