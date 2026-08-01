
def test_cont_basic_fit(distname, arg, n_fit_samples, method, fix_args):
    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname

    rng = np.random.RandomState(765456)
    rvs = distfn.rvs(size=n_fit_samples, *arg, random_state=rng)
    if fix_args:
        check_fit_args_fix(distfn, arg, rvs, method)
    else:
        check_fit_args(distfn, arg, rvs, method)

