
def test_rvs_scalar(distname, arg):
    # rvs should return a scalar when given scalar arguments (gh-12428)
    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'rv_histogram_instance'

    assert np.isscalar(distfn.rvs(*arg))
    assert np.isscalar(distfn.rvs(*arg, size=()))
    assert np.isscalar(distfn.rvs(*arg, size=None))

