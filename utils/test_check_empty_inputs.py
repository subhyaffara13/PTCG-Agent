
def test_check_empty_inputs():
    # Test that _check_empty_inputs is doing its job, at least for single-
    # sample inputs. (Multi-sample functionality is tested below.)
    # If the input sample is not empty, it should return None.
    # If the input sample is empty, it should return an array of NaNs or an
    # empty array of appropriate shape. np.mean is used as a reference for the
    # output because, like the statistics calculated by these functions,
    # it works along and "consumes" `axis` but preserves the other axes.
    for i in range(5):
        for combo in combinations_with_replacement([0, 1, 2], i):
            for axis in range(len(combo)):
                samples = (np.zeros(combo),)
                output = stats._axis_nan_policy._check_empty_inputs(samples,
                                                                    axis)
                if output is not None:
                    with warnings.catch_warnings():
                        warnings.filterwarnings(
                            "ignore", "Mean of empty slice", RuntimeWarning)
                        warnings.filterwarnings(
                            "ignore", "invalid value encountered", RuntimeWarning)
                        reference = samples[0].mean(axis=axis)
                    np.testing.assert_equal(output, reference)

