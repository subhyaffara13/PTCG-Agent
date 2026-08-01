
def cases_test_moments():
    fail_normalization = set()
    fail_higher = {'ncf'}
    fail_moment = {'johnsonsu'}  # generic `munp` is inaccurate for johnsonsu

    for distname, arg in distcont[:] + histogram_test_instances:
        if distname == 'levy_stable':
            continue

        if distname in xslow_test_moments:
            yield pytest.param(distname, arg, True, True, True, True,
                               marks=pytest.mark.xslow(reason="too slow"))
            continue

        cond1 = distname not in fail_normalization
        cond2 = distname not in fail_higher
        cond3 = distname not in fail_moment

        marks = list()
        # Currently unused, `marks` can be used to add a timeout to a test of
        # a specific distribution.  For example, this shows how a timeout could
        # be added for the 'skewnorm' distribution:
        #
        #     marks = list()
        #     if distname == 'skewnorm':
        #         marks.append(pytest.mark.timeout(300))

        yield pytest.param(distname, arg, cond1, cond2, cond3,
                           False, marks=marks)

        if not cond1 or not cond2 or not cond3:
            # Run the distributions that have issues twice, once skipping the
            # not_ok parts, once with the not_ok parts but marked as knownfail
            yield pytest.param(distname, arg, True, True, True, True,
                               marks=[pytest.mark.xfail] + marks)

