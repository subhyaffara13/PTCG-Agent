
def _boxcox_conf_interval(x, lmax, alpha):
    # Need to find the lambda for which
    #  f(x,lmbda) >= f(x,lmax) - 0.5*chi^2_alpha;1
    fac = 0.5 * distributions.chi2.ppf(1 - alpha, 1)
    target = boxcox_llf(lmax, x) - fac

    def rootfunc(lmbda, data, target):
        return boxcox_llf(lmbda, data) - target

    # Find positive endpoint of interval in which answer is to be found
    newlm = lmax + 0.5
    N = 0
    while (rootfunc(newlm, x, target) > 0.0) and (N < 500):
        newlm += 0.1
        N += 1

    if N == 500:
        raise RuntimeError("Could not find endpoint.")

    lmplus = optimize.brentq(rootfunc, lmax, newlm, args=(x, target))

    # Now find negative interval in the same way
    newlm = lmax - 0.5
    N = 0
    while (rootfunc(newlm, x, target) > 0.0) and (N < 500):
        newlm -= 0.1
        N += 1

    if N == 500:
        raise RuntimeError("Could not find endpoint.")

    lmminus = optimize.brentq(rootfunc, newlm, lmax, args=(x, target))
    return lmminus, lmplus

