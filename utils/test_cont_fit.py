
def test_cont_fit(distname, arg, method):
    run_xfail = int(os.getenv('SCIPY_XFAIL', default=False))
    run_xslow = int(os.getenv('SCIPY_XSLOW', default=False))

    if distname in failing_fits[method] and not run_xfail:
        # The generic `fit` method can't be expected to work perfectly for all
        # distributions, data, and guesses. Some failures are expected.
        msg = "Failure expected; set environment variable SCIPY_XFAIL=1 to run."
        pytest.xfail(msg)

    if distname in xslow_fits[method] and not run_xslow:
        msg = "Very slow; set environment variable SCIPY_XSLOW=1 to run."
        pytest.skip(msg)

    distfn = getattr(stats, distname)

    truearg = np.hstack([arg, [0.0, 1.0]])
    diffthreshold = np.max(np.vstack([truearg*thresh_percent,
                                      np.full(distfn.numargs+2, thresh_min)]),
                           0)

    for fit_size in fit_sizes:
        # Note that if a fit succeeds, the other fit_sizes are skipped
        rng = np.random.default_rng(1234)

        with np.errstate(all='ignore'):
            rvs = distfn.rvs(size=fit_size, *arg, random_state=rng)
            if method == 'MLE' and distfn.name in mle_use_floc0:
                kwds = {'floc': 0}
            else:
                kwds = {}
            # start with default values
            est = distfn.fit(rvs, method=method, **kwds)
            if method == 'MLE':
                # Trivial test of the use of CensoredData.  The fit() method
                # will check that data contains no actual censored data, and
                # do a regular uncensored fit.
                data1 = stats.CensoredData(rvs)
                est1 = distfn.fit(data1, **kwds)
                msg = ('Different results fitting uncensored data wrapped as'
                       f' CensoredData: {distfn.name}: est={est} est1={est1}')
                assert_allclose(est1, est, rtol=1e-10, err_msg=msg)
            if method == 'MLE' and distname not in fail_interval_censored:
                # Convert the first `nic` values in rvs to interval-censored
                # values. The interval is small, so est2 should be close to
                # est.
                nic = 15
                interval = np.column_stack((rvs, rvs))
                interval[:nic, 0] *= 0.99
                interval[:nic, 1] *= 1.01
                interval.sort(axis=1)
                data2 = stats.CensoredData(interval=interval)
                est2 = distfn.fit(data2, **kwds)
                msg = ('Different results fitting interval-censored'
                       f' data: {distfn.name}: est={est} est2={est2}')
                assert_allclose(est2, est, rtol=0.05, err_msg=msg)

        diff = est - truearg

        # threshold for location
        diffthreshold[-2] = np.max([np.abs(rvs.mean())*thresh_percent,
                                    thresh_min])

        if np.any(np.isnan(est)):
            raise AssertionError('nan returned in fit')
        else:
            if np.all(np.abs(diff) <= diffthreshold):
                break
    else:
        txt = f'parameter: {str(truearg)}\n'
        txt += f'estimated: {str(est)}\n'
        txt += f'diff     : {str(diff)}\n'
        raise AssertionError(f'fit not very good in {distfn.name}\n' + txt)

