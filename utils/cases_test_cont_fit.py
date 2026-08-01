
def cases_test_cont_fit():
    # this tests the closeness of the estimated parameters to the true
    # parameters with fit method of continuous distributions
    # Note: is slow, some distributions don't converge with sample
    # size <= 10000
    for distname, arg in distcont:
        if distname not in skip_fit:
            yield distname, arg

