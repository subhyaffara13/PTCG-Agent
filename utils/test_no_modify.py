
def test_no_modify():
    # Test that Triangulation does not modify triangles array passed to it.
    triangles = np.array([[3, 2, 0], [3, 1, 0]], dtype=np.int32)
    points = np.array([(0, 0), (0, 1.1), (1, 0), (1, 1)])

    old_triangles = triangles.copy()
    mtri.Triangulation(points[:, 0], points[:, 1], triangles).edges
    assert_array_equal(old_triangles, triangles)

