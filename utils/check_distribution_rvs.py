
def check_distribution_rvs(dist, args, alpha, rvs):
    # dist is either a cdf function or name of a distribution in scipy.stats.
    # args are the args for scipy.stats.dist(*args)
    # alpha is a significance level, ~0.01
    # rvs is array_like of random variables
    # test from scipy.stats.tests
    # this version reuses existing random variables
    D, pval = stats.kstest(rvs, dist, args=args, N=1000)
    if (pval < alpha):
        # The rvs passed in failed the K-S test, which _could_ happen
        # but is unlikely if alpha is small enough.
        # Repeat the test with a new sample of rvs.
        # Generate 1000 rvs, perform a K-S test that the new sample of rvs
        # are distributed according to the distribution.
        D, pval = stats.kstest(dist, dist, args=args, N=1000)
        npt.assert_(pval > alpha, "D = " + str(D) + "; pval = " + str(pval) +
                    "; alpha = " + str(alpha) + "\nargs = " + str(args))

