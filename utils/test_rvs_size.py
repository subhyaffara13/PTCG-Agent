
def test_rvs_size(size):
    # As the `rvs` method is present in the base class and shared between
    # all the classes, we can just test with one of the methods.
    rng = TransformedDensityRejection(StandardNormal())
    if size is None:
        assert np.isscalar(rng.rvs(size))
    else:
        if np.isscalar(size):
            size = (size, )
        assert rng.rvs(size).shape == size

