
def test_validator_valid(validator, arg, target):
    res = validator(arg)
    if isinstance(target, np.ndarray):
        np.testing.assert_equal(res, target)
    elif not isinstance(target, Cycler):
        assert res == target
    else:
        # Cyclers can't simply be asserted equal. They don't implement __eq__
        assert list(res) == list(target)

