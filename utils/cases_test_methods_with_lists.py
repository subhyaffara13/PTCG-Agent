
def cases_test_methods_with_lists():
    for distname, arg in distcont:
        if distname in slow_with_lists:
            yield pytest.param(distname, arg, marks=pytest.mark.slow)
        else:
            yield distname, arg

