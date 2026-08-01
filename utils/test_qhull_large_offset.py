
def test_qhull_large_offset():
    # github issue 8682.
    x = np.asarray([0, 1, 0, 1, 0.5])
    y = np.asarray([0, 0, 1, 1, 0.5])

    offset = 1e10
    triang = mtri.Triangulation(x, y)
    triang_offset = mtri.Triangulation(x + offset, y + offset)
    assert len(triang.triangles) == len(triang_offset.triangles)

