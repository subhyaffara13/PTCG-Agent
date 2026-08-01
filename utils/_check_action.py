
def _check_action(fun, args, action):
    # TODO: special expert should correct
    # the coercion at the true location?
    args = np.asarray(args, dtype=np.dtype("long"))
    if action == 'warn':
        with pytest.warns(sc.SpecialFunctionWarning):
            fun(*args)
    elif action == 'raise':
        with assert_raises(sc.SpecialFunctionError):
            fun(*args)
    else:
        # action == 'ignore', make sure there are no warnings/exceptions
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fun(*args)

