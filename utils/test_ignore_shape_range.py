
def test_ignore_shape_range():
    msg = "No generator is defined for the shape parameters"
    with pytest.raises(ValueError, match=msg):
        rng = FastGeneratorInversion(stats.t(0.03))
    rng = FastGeneratorInversion(stats.t(0.03), ignore_shape_range=True)
    # we can ignore the recommended range of shape parameters
    # but u-error can be expected to be too large in that case
    u_err, _ = rng.evaluate_error(size=1000, random_state=234)
    assert u_err >= 1e-6

