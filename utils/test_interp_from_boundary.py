
def test_interp_from_boundary(interpolation_class, simplex_tolerance):
    """Test that SciPy can interpolate to a regular grid from the boundary.

    Based on gh-21910
    """
    coords = np.block(
        [[0, np.arange(400, 500), np.zeros(100), 800],
         [0, np.zeros(100), np.arange(400, 500), 800]]
    )
    values = np.ones(202)
    interpolator = interpolation_class(coords.T, values)
    results = interpolator(
        np.mgrid[:500, :500].T, simplex_tolerance=simplex_tolerance
    )
    num_nans = np.count_nonzero(np.isnan(results))
    if simplex_tolerance == 1:
        # The default tolerance doesn't work when filling from a
        # dense boundary
        assert num_nans > 0
    else:
        # The larger tolerance allows QHull to assign a simplex
        # for each point
        assert num_nans == 0

