
def test_non_broadcastable(hypotest, args, kwds, n_samples, n_outputs, paired,
                           unpacker, axis):
    # test for correct error message when shapes are not broadcastable
    rng = np.random.default_rng(91359824598245)
    get_samples = True
    while get_samples:
        samples = [rng.random(size=rng.integers(2, 100, size=2))
                   for i in range(n_samples)]
        # if samples are broadcastable, try again
        get_samples = _check_arrays_broadcastable(samples, axis=axis)

    message = "Array shapes are incompatible for broadcasting."
    with pytest.raises(ValueError, match=message):
        hypotest(*samples, *args, axis=axis, **kwds)

    if not paired:  # there's another test for paired-sample statistics
        return

    # Previously, paired sample statistics did not raise an error
    # message when the shapes were broadcastable except along `axis`
    # https://github.com/scipy/scipy/pull/19578#pullrequestreview-1766857165
    shape = rng.integers(2, 10, size=2)
    most_samples = [rng.random(size=shape) for i in range(n_samples-1)]
    shape = list(shape)
    shape[axis] += 1
    other_sample = rng.random(size=shape)
    with pytest.raises(ValueError, match=message):
        hypotest(other_sample, *most_samples, *args, axis=axis, **kwds)

