
def test_integration_reduction_dynamic():
    triangle = Polygon(Point(0, 3), Point(5, 3), Point(1, 1))
    facets = triangle.sides
    a, b = hyperplane_parameters(triangle)[0]
    x0 = facets[0].points[0]
    monomial_values = [[0, 0, 0, 0], [1, 0, 0, 5],\
                       [y, 0, 1, 15], [x, 1, 0, None]]

    assert integration_reduction_dynamic(facets, 0, a, b, x, 1, (x, y), 1,\
                                         0, 1, x0, monomial_values, 3) == Rational(25, 2)
    assert integration_reduction_dynamic(facets, 0, a, b, 0, 1, (x, y), 1,\
                                         0, 1, x0, monomial_values, 3) == 0

