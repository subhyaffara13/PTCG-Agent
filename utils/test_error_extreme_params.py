
def test_error_extreme_params(distname, args):
    # take extreme parameters where u-error might not be below the tolerance
    # due to limitations of floating point arithmetic
    with warnings.catch_warnings():
        # filter the warnings thrown by UNU.RAN for such extreme parameters
        warnings.simplefilter("ignore", RuntimeWarning)
        dist = getattr(stats, distname)(*args)
        rng = FastGeneratorInversion(dist)
    u_error, x_error = rng.evaluate_error(
        size=10_000, random_state=980732462809709732623, x_error=True
    )
    if u_error >= 2.5 * 1e-10:
        assert x_error < 1e-9

