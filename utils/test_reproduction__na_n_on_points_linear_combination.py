
def test_reproduction_NaN_on_points_linear_combination(
    simplex_tolerance, interpolator_factory
):
    """Test that SciPy can interpolate to the edge of a triangle.

    Based on gh-22831
    """
    inputs = np.array([[ 0.       ,  0.       ],
                      [ 0.       ,  0.008016],
                      [ 3.       , -2.       ]])
    values = np.ones(len(inputs))
    # Create the interpolator
    interpolator = interpolator_factory(inputs, values)
    t1 = 0.6
    p1 = inputs[0]
    p2 = inputs[2]
    point_on_edge = p1 + t1 * (p2 - p1)
    value = interpolator(*point_on_edge, simplex_tolerance=simplex_tolerance)
    if simplex_tolerance == 1:
        assert np.isnan(value)
    else:
        assert np.isfinite(value)

