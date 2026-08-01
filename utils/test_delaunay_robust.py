
def test_delaunay_robust():
    # Fails when mtri.Triangulation uses matplotlib.delaunay, works when using
    # qhull.
    tri_points = np.array([
        [0.8660254037844384, -0.5000000000000004],
        [0.7577722283113836, -0.5000000000000004],
        [0.6495190528383288, -0.5000000000000003],
        [0.5412658773652739, -0.5000000000000003],
        [0.811898816047911, -0.40625000000000044],
        [0.7036456405748561, -0.4062500000000004],
        [0.5953924651018013, -0.40625000000000033]])
    test_points = np.asarray([
        [0.58, -0.46],
        [0.65, -0.46],
        [0.65, -0.42],
        [0.7, -0.48],
        [0.7, -0.44],
        [0.75, -0.44],
        [0.8, -0.48]])

    # Utility function that indicates if a triangle defined by 3 points
    # (xtri, ytri) contains the test point xy.  Avoid calling with a point that
    # lies on or very near to an edge of the triangle.
    def tri_contains_point(xtri, ytri, xy):
        tri_points = np.vstack((xtri, ytri)).T
        return Path(tri_points).contains_point(xy)

    # Utility function that returns how many triangles of the specified
    # triangulation contain the test point xy.  Avoid calling with a point that
    # lies on or very near to an edge of any triangle in the triangulation.
    def tris_contain_point(triang, xy):
        return sum(tri_contains_point(triang.x[tri], triang.y[tri], xy)
                   for tri in triang.triangles)

    # Using matplotlib.delaunay, an invalid triangulation is created with
    # overlapping triangles; qhull is OK.
    triang = mtri.Triangulation(tri_points[:, 0], tri_points[:, 1])
    for test_point in test_points:
        assert tris_contain_point(triang, test_point) == 1

    # If ignore the first point of tri_points, matplotlib.delaunay throws a
    # KeyError when calculating the convex hull; qhull is OK.
    triang = mtri.Triangulation(tri_points[1:, 0], tri_points[1:, 1])

