
def test_integration_reduction():
    triangle = Polygon(Point(0, 3), Point(5, 3), Point(1, 1))
    facets = triangle.sides
    a, b = hyperplane_parameters(triangle)[0]
    assert integration_reduction(facets, 0, a, b, 1, (x, y), 0) == 5
    assert integration_reduction(facets, 0, a, b, 0, (x, y), 0) == 0

