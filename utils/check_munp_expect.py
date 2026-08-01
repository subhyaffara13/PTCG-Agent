
def check_munp_expect(dist, args, msg):
    # If _munp is overridden, test a higher moment. (Before gh-18634, some
    # distributions had issues with moments 5 and higher.)
    if dist._munp.__func__ != stats.rv_continuous._munp:
        res = dist.moment(5, *args)  # shouldn't raise an error
        ref = dist.expect(lambda x: x ** 5, args, lb=-np.inf, ub=np.inf)
        if not np.isfinite(res):  # could be valid; automated test can't know
            return
        # loose tolerance, mostly to see whether _munp returns *something*
        assert_allclose(res, ref, atol=1e-10, rtol=1e-4,
                        err_msg=msg + ' - higher moment / _munp')

