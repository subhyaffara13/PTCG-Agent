
def check_fit_args(distfn, arg, rvs, method):
    with np.errstate(all='ignore'), warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning,
                   message="The shape parameter of the erlang")
        warnings.filterwarnings("ignore", category=RuntimeWarning,
                   message="floating point number truncated")
        vals = distfn.fit(rvs, method=method)
        vals2 = distfn.fit(rvs, optimizer='powell', method=method)
    # Only check the length of the return; accuracy tested in test_fit.py
    npt.assert_(len(vals) == 2+len(arg))
    npt.assert_(len(vals2) == 2+len(arg))

