
def check_pickling(distfn, args):
    # check that a distribution instance pickles and unpickles
    # pay special attention to the random_state property

    # save the random_state (restore later)
    rndm = distfn.random_state

    # check unfrozen
    distfn.random_state = 1234
    distfn.rvs(*args, size=8)
    s = pickle.dumps(distfn)
    r0 = distfn.rvs(*args, size=8)

    unpickled = pickle.loads(s)
    r1 = unpickled.rvs(*args, size=8)
    npt.assert_equal(r0, r1)

    # also smoke test some methods
    medians = [distfn.ppf(0.5, *args), unpickled.ppf(0.5, *args)]
    npt.assert_equal(medians[0], medians[1])
    npt.assert_equal(distfn.cdf(medians[0], *args),
                     unpickled.cdf(medians[1], *args))

    # check frozen pickling/unpickling with rvs
    frozen_dist = distfn(*args)
    pkl = pickle.dumps(frozen_dist)
    unpickled = pickle.loads(pkl)

    r0 = frozen_dist.rvs(size=8)
    r1 = unpickled.rvs(size=8)
    npt.assert_equal(r0, r1)

    # check pickling/unpickling of .fit method
    if hasattr(distfn, "fit"):
        fit_function = distfn.fit
        pickled_fit_function = pickle.dumps(fit_function)
        unpickled_fit_function = pickle.loads(pickled_fit_function)
        assert fit_function.__name__ == unpickled_fit_function.__name__ == "fit"

    # restore the random_state
    distfn.random_state = rndm


def check_pickling(distfn, args):
    # check that a distribution instance pickles and unpickles
    # pay special attention to the random_state property

    # save the random_state (restore later)
    rndm = distfn.random_state

    distfn.random_state = 1234
    distfn.rvs(*args, size=8)
    s = pickle.dumps(distfn)
    r0 = distfn.rvs(*args, size=8)

    unpickled = pickle.loads(s)
    r1 = unpickled.rvs(*args, size=8)
    assert_equal(r0, r1)

    # restore the random_state
    distfn.random_state = rndm

