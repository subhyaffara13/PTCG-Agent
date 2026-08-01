
def ttest_data_axis_strategy(draw):
    # draw an array under shape and value constraints
    elements = dict(allow_nan=False, allow_infinity=False)
    shape = npst.array_shapes(min_dims=1, min_side=2)
    # The test that uses this, `test_pvalue_ci`, uses `float64` to test
    # extreme `alpha`. It could be adjusted to test a dtype-dependent
    # range of `alpha` if this strategy is needed to generate other floats.
    data = draw(npst.arrays(dtype=np.float64, elements=elements, shape=shape))

    # determine axes over which nonzero variance can be computed accurately
    ok_axes = []
    # Locally, I don't need catch_warnings or simplefilter, and I can just
    # suppress RuntimeWarning. I include all that in hope of getting the same
    # behavior on CI.
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        for axis in range(len(data.shape)):
            with contextlib.suppress(Exception):
                var = stats.moment(data, order=2, axis=axis)
                if np.all(var > 0) and np.all(np.isfinite(var)):
                    ok_axes.append(axis)
    # if there are no valid axes, tell hypothesis to try a different example
    hypothesis.assume(ok_axes)

    # draw one of the valid axes
    axis = draw(hypothesis.strategies.sampled_from(ok_axes))

    return data, axis

