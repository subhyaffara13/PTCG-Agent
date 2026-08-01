
def test_methods_with_lists(method, distname, args):
    # Test that the continuous distributions can accept Python lists
    # as arguments.
    dist = getattr(stats, distname)
    f = getattr(dist, method)
    if distname == 'invweibull' and method.startswith('log'):
        x = [1.5, 2]
    else:
        x = [0.1, 0.2]

    shape2 = [[a]*2 for a in args]
    loc = [0, 0.1]
    scale = [1, 1.01]
    result = f(x, *shape2, loc=loc, scale=scale)
    npt.assert_allclose(result,
                        [f(*v) for v in zip(x, *shape2, loc, scale)],
                        rtol=1e-14, atol=5e-14)


def test_methods_with_lists(method, distname, args):
    # Test that the discrete distributions can accept Python lists
    # as arguments.
    try:
        dist = getattr(stats, distname)
    except TypeError:
        return
    dist_method = getattr(dist, method)
    if method in ['ppf', 'isf']:
        z = [0.1, 0.2]
    else:
        z = [0, 1]
    p2 = [[p]*2 for p in args]
    loc = [0, 1]
    result = dist_method(z, *p2, loc=loc)
    npt.assert_allclose(result,
                        [dist_method(*v) for v in zip(z, *p2, loc)],
                        rtol=1e-15, atol=1e-15)

