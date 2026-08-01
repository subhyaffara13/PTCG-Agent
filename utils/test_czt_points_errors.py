
def test_czt_points_errors(m):
    # Invalid number of points
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        czt_points(m)

