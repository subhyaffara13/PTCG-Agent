
def cases_test_cont_basic():
    for distname, arg in distcont[:] + histogram_test_instances:
        if distname == 'levy_stable':  # fails; tested separately
            continue
        if distname in slow_test_cont_basic:
            yield pytest.param(distname, arg, marks=pytest.mark.slow)
        elif distname in xslow_test_cont_basic:
            yield pytest.param(distname, arg, marks=pytest.mark.xslow)
        else:
            yield distname, arg

