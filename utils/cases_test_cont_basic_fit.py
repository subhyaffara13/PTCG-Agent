
def cases_test_cont_basic_fit():
    slow = pytest.mark.slow
    xslow = pytest.mark.xslow
    fail = pytest.mark.skip(reason="Test fails and may be slow.")
    skip = pytest.mark.skip(reason="Test too slow to run to completion (>10m).")

    for distname, arg in distcont[:] + histogram_test_instances:
        for method in ["MLE", "MM"]:
            for fix_args in [True, False]:
                if method == 'MLE' and distname in slow_fit_mle:
                    yield pytest.param(distname, arg, method, fix_args, marks=slow)
                    continue
                if method == 'MLE' and distname in xslow_fit_mle:
                    yield pytest.param(distname, arg, method, fix_args, marks=xslow)
                    continue
                if method == 'MLE' and distname in xfail_fit_mle:
                    yield pytest.param(distname, arg, method, fix_args, marks=fail)
                    continue
                if method == 'MLE' and distname in skip_fit_mle:
                    yield pytest.param(distname, arg, method, fix_args, marks=skip)
                    continue
                if method == 'MM' and distname in slow_fit_mm:
                    yield pytest.param(distname, arg, method, fix_args, marks=slow)
                    continue
                if method == 'MM' and distname in xslow_fit_mm:
                    yield pytest.param(distname, arg, method, fix_args, marks=xslow)
                    continue
                if method == 'MM' and distname in xfail_fit_mm:
                    yield pytest.param(distname, arg, method, fix_args, marks=fail)
                    continue
                if method == 'MM' and distname in skip_fit_mm:
                    yield pytest.param(distname, arg, method, fix_args, marks=skip)
                    continue

                yield distname, arg, method, fix_args

