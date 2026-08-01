
def test_performance():
    # Compare performance results to those listed in
    # [Cheng & Li, IMA J. Num. An. 29, 814 (2008)]
    # and
    # [W. La Cruz, J.M. Martinez, M. Raydan, Math. Comp. 75, 1429 (2006)].
    # and those produced by dfsane.f from M. Raydan's website.
    #
    # Where the results disagree, the largest limits are taken.

    e_a = 1e-5
    e_r = 1e-4

    table_1 = [
        dict(F=F_1, x0=x0_1, n=1000, nit=5, nfev=5),
        dict(F=F_1, x0=x0_1, n=10000, nit=2, nfev=2),
        dict(F=F_2, x0=x0_2, n=500, nit=11, nfev=11),
        dict(F=F_2, x0=x0_2, n=2000, nit=11, nfev=11),
        # dict(F=F_4, x0=x0_4, n=999, nit=243, nfev=1188) removed:
        # too sensitive to rounding errors
        # Results from dfsane.f; papers list nit=3, nfev=3
        dict(F=F_6, x0=x0_6, n=100, nit=6, nfev=6),
        # Must have n%3==0, typo in papers?
        dict(F=F_7, x0=x0_7, n=99, nit=23, nfev=29),
        # Must have n%3==0, typo in papers?
        dict(F=F_7, x0=x0_7, n=999, nit=23, nfev=29),
        # Results from dfsane.f; papers list nit=nfev=6?
        dict(F=F_9, x0=x0_9, n=100, nit=12, nfev=18),
        dict(F=F_9, x0=x0_9, n=1000, nit=12, nfev=18),
        # Results from dfsane.f; papers list nit=2, nfev=12
        dict(F=F_10, x0=x0_10, n=1000, nit=5, nfev=5),
    ]

    # Check also scaling invariance
    for xscale, yscale, line_search in itertools.product(
        [1.0, 1e-10, 1e10], [1.0, 1e-10, 1e10], ['cruz', 'cheng']
    ):
        for problem in table_1:
            n = problem['n']
            def func(x, n):
                return yscale * problem['F'](x / xscale, n)
            args = (n,)
            x0 = problem['x0'](n) * xscale

            fatol = np.sqrt(n) * e_a * yscale + e_r * np.linalg.norm(func(x0, n))

            sigma_eps = 1e-10 * min(yscale/xscale, xscale/yscale)
            sigma_0 = xscale/yscale

            with np.errstate(over='ignore'):
                sol = root(func, x0, args=args,
                           options=dict(ftol=0, fatol=fatol, maxfev=problem['nfev'] + 1,
                                        sigma_0=sigma_0, sigma_eps=sigma_eps,
                                        line_search=line_search),
                           method='DF-SANE')

            err_msg = repr(
                [xscale, yscale, line_search, problem, np.linalg.norm(func(sol.x, n)),
                 fatol, sol.success, sol.nit, sol.nfev]
            )
            assert sol.success, err_msg
            # nfev+1: dfsane.f doesn't count first eval
            assert sol.nfev <= problem['nfev'] + 1, err_msg
            assert sol.nit <= problem['nit'], err_msg
            assert np.linalg.norm(func(sol.x, n)) <= fatol, err_msg

