
def test_kdtree_complex_data():
    # Test that KDTree rejects complex input points (gh-9108)
    points = np.random.rand(10, 2).view(complex)

    with pytest.raises(TypeError, match="complex data"):
        t = KDTree(points)

    t = KDTree(points.real)

    with pytest.raises(TypeError, match="complex data"):
        t.query(points)

    with pytest.raises(TypeError, match="complex data"):
        t.query_ball_point(points, r=1)

