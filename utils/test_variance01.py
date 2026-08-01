
def test_variance01(xp):
    with np.errstate(all='ignore'):
        for type in types:
            dtype = getattr(xp, type)
            input = xp.asarray([], dtype=dtype)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", "Mean of empty slice", RuntimeWarning)
                output = ndimage.variance(input)
            assert xp.isnan(output)

