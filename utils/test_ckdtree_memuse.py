
def test_ckdtree_memuse():
    # unit test adaptation of gh-5630

    # NOTE: this will fail when run via valgrind,
    # because rss is no longer a reliable memory usage indicator.
    # It was also observed to be flaky under ASan.

    try:
        import resource
    except ImportError:
        # resource is not available on Windows
        return
    # Make some data
    dx, dy = 0.05, 0.05
    y, x = np.mgrid[slice(1, 5 + dy, dy),
                    slice(1, 5 + dx, dx)]
    z = np.sin(x)**10 + np.cos(10 + y*x) * np.cos(x)
    z_copy = np.empty_like(z)
    z_copy[:] = z
    # Place FILLVAL in z_copy at random number of random locations
    FILLVAL = 99.
    mask = np.random.randint(0, z.size, np.random.randint(50) + 5)
    z_copy.flat[mask] = FILLVAL
    igood = np.vstack(np.nonzero(x != FILLVAL)).T
    ibad = np.vstack(np.nonzero(x == FILLVAL)).T
    mem_use = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # burn-in
    for i in range(10):
        tree = cKDTree(igood)
    # count memleaks while constructing and querying cKDTree
    num_leaks = 0
    for i in range(100):
        mem_use = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        tree = cKDTree(igood)
        dist, iquery = tree.query(ibad, k=4, p=2)
        new_mem_use = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if new_mem_use > mem_use:
            num_leaks += 1
    # ideally zero leaks, but errors might accidentally happen
    # outside cKDTree
    assert_(num_leaks < 10)

