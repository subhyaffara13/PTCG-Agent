
def test_rvs_broadcast(dist, shape_args):
    if dist in ['gausshyper', 'studentized_range']:
        pytest.skip("too slow")

    if dist in ['rel_breitwigner'] and _IS_32BIT:
        # gh18414
        pytest.skip("fails on Linux 32-bit")

    # If shape_only is True, it means the _rvs method of the
    # distribution uses more than one random number to generate a random
    # variate.  That means the result of using rvs with broadcasting or
    # with a nontrivial size will not necessarily be the same as using the
    # numpy.vectorize'd version of rvs(), so we can only compare the shapes
    # of the results, not the values.
    # Whether or not a distribution is in the following list is an
    # implementation detail of the distribution, not a requirement.  If
    # the implementation the rvs() method of a distribution changes, this
    # test might also have to be changed.
    shape_only = dist in ['argus', 'betaprime', 'dgamma', 'dpareto_lognorm', 'dweibull',
                          'exponnorm', 'genhyperbolic', 'geninvgauss', 'landau',
                          'levy_stable', 'nct', 'norminvgauss', 'rice',
                          'skewnorm', 'semicircular', 'gennorm', 'loggamma']

    distfunc = getattr(stats, dist)
    loc = np.zeros(2)
    scale = np.ones((3, 1))
    nargs = distfunc.numargs
    allargs = []
    bshape = [3, 2]
    # Generate shape parameter arguments...
    for k in range(nargs):
        shp = (k + 4,) + (1,)*(k + 2)
        allargs.append(shape_args[k]*np.ones(shp))
        bshape.insert(0, k + 4)
    allargs.extend([loc, scale])
    # bshape holds the expected shape when loc, scale, and the shape
    # parameters are all broadcast together.

    check_rvs_broadcast(distfunc, dist, allargs, bshape, shape_only, 'd')


def test_rvs_broadcast(dist, shape_args):
    # If shape_only is True, it means the _rvs method of the
    # distribution uses more than one random number to generate a random
    # variate.  That means the result of using rvs with broadcasting or
    # with a nontrivial size will not necessarily be the same as using the
    # numpy.vectorize'd version of rvs(), so we can only compare the shapes
    # of the results, not the values.
    # Whether or not a distribution is in the following list is an
    # implementation detail of the distribution, not a requirement.  If
    # the implementation the rvs() method of a distribution changes, this
    # test might also have to be changed.
    shape_only = dist in ['betabinom', 'betanbinom', 'skellam', 'yulesimon',
                          'dlaplace', 'nchypergeom_fisher',
                          'nchypergeom_wallenius', 'poisson_binom']
    try:
        distfunc = getattr(stats, dist)
    except TypeError:
        distfunc = dist
        dist = f'rv_discrete(values=({dist.xk!r}, {dist.pk!r}))'
    loc = np.zeros(2)
    nargs = distfunc.numargs
    allargs = []
    bshape = []

    if dist == 'poisson_binom':
        # normal rules apply except the last axis of `p` is ignored
        p = np.full((3, 1, 10), 0.5)
        allargs = (p, loc)
        bshape = (3, 2)
        check_rvs_broadcast(distfunc, dist, allargs,
                            bshape, shape_only, [np.dtype(int)])
        return

    # Generate shape parameter arguments...
    for k in range(nargs):
        shp = (k + 3,) + (1,)*(k + 1)
        param_val = shape_args[k]
        allargs.append(np.full(shp, param_val))
        bshape.insert(0, shp[0])
    allargs.append(loc)
    bshape.append(loc.size)
    # bshape holds the expected shape when loc, scale, and the shape
    # parameters are all broadcast together.
    check_rvs_broadcast(
        distfunc, dist, allargs, bshape, shape_only, [np.dtype(int)]
    )

