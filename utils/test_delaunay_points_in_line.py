
def test_delaunay_points_in_line():
    # Cannot triangulate points that are all in a straight line, but check
    # that delaunay code fails gracefully.
    x = np.linspace(0.0, 10.0, 11)
    y = np.linspace(0.0, 10.0, 11)
    with pytest.raises(RuntimeError):
        mtri.Triangulation(x, y)

    # Add an extra point not on the line and the triangulation is OK.
    x = np.append(x, 2.0)
    y = np.append(y, 8.0)
    mtri.Triangulation(x, y)

