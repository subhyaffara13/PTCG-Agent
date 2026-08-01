
def _weibull_fit_check(params, x):
    # Refine the fit returned by `weibull_min.fit` to ensure that the first
    # order necessary conditions are satisfied. If not, raise an error.
    # Here, use `m` for the shape parameter to be consistent with [7]
    # and avoid confusion with `c` as defined in [7].
    n = len(x)
    m, u, s = params

    def dnllf_dm(m, u):
        # Partial w.r.t. shape w/ optimal scale. See [7] Equation 5.
        xu = x-u
        return (1/m - (xu**m*np.log(xu)).sum()/(xu**m).sum()
                + np.log(xu).sum()/n)

    def dnllf_du(m, u):
        # Partial w.r.t. loc w/ optimal scale. See [7] Equation 6.
        xu = x-u
        return (m-1)/m*(xu**-1).sum() - n*(xu**(m-1)).sum()/(xu**m).sum()

    def get_scale(m, u):
        # Partial w.r.t. scale solved in terms of shape and location.
        # See [7] Equation 7.
        return ((x-u)**m/n).sum()**(1/m)

    def dnllf(params):
        # Partial derivatives of the NLLF w.r.t. parameters, i.e.
        # first order necessary conditions for MLE fit.
        return [dnllf_dm(*params), dnllf_du(*params)]

    suggestion = ("Maximum likelihood estimation is known to be challenging "
                  "for the three-parameter Weibull distribution. Consider "
                  "performing a custom goodness-of-fit test using "
                  "`scipy.stats.monte_carlo_test`.")

    if np.allclose(u, np.min(x)) or m < 1:
        # The critical values provided by [7] don't seem to control the
        # Type I error rate in this case. Error out.
        message = ("Maximum likelihood estimation has converged to "
                   "a solution in which the location is equal to the minimum "
                   "of the data, the shape parameter is less than 2, or both. "
                   "The table of critical values in [7] does not "
                   "include this case. " + suggestion)
        raise ValueError(message)

    try:
        # Refine the MLE / verify that first-order necessary conditions are
        # satisfied. If so, the critical values provided in [7] seem reliable.
        with np.errstate(over='raise', invalid='raise'):
            res = optimize.root(dnllf, params[:-1])

        message = ("Solution of MLE first-order conditions failed: "
                   f"{res.message}. `anderson` cannot continue. " + suggestion)
        if not res.success:
            raise ValueError(message)

    except (FloatingPointError, ValueError) as e:
        message = ("An error occurred while fitting the Weibull distribution "
                   "to the data, so `anderson` cannot continue. " + suggestion)
        raise ValueError(message) from e

    m, u = res.x
    s = get_scale(m, u)
    return m, u, s

