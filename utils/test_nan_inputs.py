
def test_nan_inputs(func):
    args = (np.nan,)*func.nin
    with warnings.catch_warnings():
        # Ignore warnings about unsafe casts from legacy wrappers
        warnings.filterwarnings(
            "ignore",
            "floating point number truncated to an integer",
            RuntimeWarning
        )
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                res = func(*args)
        except TypeError:
            # One of the arguments doesn't take real inputs
            return
    if func in POSTPROCESSING:
        res = POSTPROCESSING[func](*res)

    msg = f"got {res} instead of nan"
    assert_array_equal(np.isnan(res), True, err_msg=msg)

