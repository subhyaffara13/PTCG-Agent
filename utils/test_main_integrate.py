
def test_main_integrate():
    triangle = Polygon((0, 3), (5, 3), (1, 1))
    facets = triangle.sides
    hp_params = hyperplane_parameters(triangle)
    assert main_integrate(x**2 + y**2, facets, hp_params) == Rational(325, 6)
    assert main_integrate(x**2 + y**2, facets, hp_params, max_degree=1) == \
        {0: 0, 1: 5, y: Rational(35, 3), x: 10}

