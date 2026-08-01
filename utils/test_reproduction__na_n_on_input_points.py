
def test_reproduction_NaN_on_input_points(
        simplex_tolerance, interpolator_factory
):
    """Test that SciPy can interpolate to the input points.

    Based on gh-21279.
    Should probably be generalized to a hypothesis test.
    """
    inputs = np.array([[-0.004167550182114899, 0.3422659245670766],
                       [-0.0015600025635140293, 0.2293516674374961],
                       [-0.0014546640482194341, 0.22508674815327132],
                       [-0.0014520968885052055, 0.2212277697065949]])
    values = np.ones_like(inputs[:, 0])
    interpolator = interpolator_factory(inputs, values)
    results = interpolator(inputs, simplex_tolerance=simplex_tolerance)
    if simplex_tolerance == 1:
        assert np.any(np.isnan(results))
    else:
        assert np.all(np.isfinite(results))

