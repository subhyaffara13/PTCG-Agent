
def check_random_state_property(distfn, args):
    # check the random_state attribute of a distribution *instance*

    # baseline: this relies on the global state
    np.random.seed(1234)  # valid use of np.random.seed
    distfn.random_state = None
    r0 = distfn.rvs(*args, size=8)

    # use an explicit instance-level random_state
    distfn.random_state = 1234
    r1 = distfn.rvs(*args, size=8)
    npt.assert_equal(r0, r1)

    distfn.random_state = np.random.RandomState(1234)
    r2 = distfn.rvs(*args, size=8)
    npt.assert_equal(r0, r2)

    # check that np.random.Generator can be used (numpy >= 1.17)
    if hasattr(np.random, 'default_rng'):
        # obtain a np.random.Generator object
        rng = np.random.default_rng(1234)
        distfn.rvs(*args, size=1, random_state=rng)

    # can override the instance-level random_state for an individual .rvs call
    distfn.random_state = 2
    orig_state = distfn.random_state.get_state()

    r3 = distfn.rvs(*args, size=8, random_state=np.random.RandomState(1234))
    npt.assert_equal(r0, r3)

    # ... and that does not alter the instance-level random_state!
    npt.assert_equal(distfn.random_state.get_state(), orig_state)

