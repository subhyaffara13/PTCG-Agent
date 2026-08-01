
def test_nonfinite(func, numargs):

    rng = np.random.default_rng(1701299355559735)
    func = getattr(sp, func)
    args_choices = [(float(x), np.nan, np.inf, -np.inf) for x in rng.random(numargs)]

    for args in itertools.product(*args_choices):
        res = func(*args)

        if any(np.isnan(x) for x in args):
            # Nan inputs should result to nan output
            assert_equal(res, np.nan)
        else:
            # All other inputs should return something (but not
            # raise exceptions or cause hangs)
            pass


def test_nonfinite():
    pts = [0.0, -0.0, np.inf]
    std = [-np.inf, np.inf, np.inf]
    assert_equal(sc.digamma(pts), std)
    assert_(all(np.isnan(sc.digamma([-np.inf, -1]))))

