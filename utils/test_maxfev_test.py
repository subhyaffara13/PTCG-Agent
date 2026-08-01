
def test_maxfev_test():
    rng = np.random.default_rng(271707100830272976862395227613146332411)

    def cost(x):
        return rng.random(1) * 1000  # never converged problem

    for imaxfev in [1, 10, 50]:
        # "TNC" and "L-BFGS-B" also supports max function evaluation, but
        # these may violate the limit because of evaluating gradients
        # by numerical differentiation. See the discussion in PR #14805.
        for method in ['Powell', 'Nelder-Mead']:
            result = optimize.minimize(cost, rng.random(10),
                                       method=method,
                                       options={'maxfev': imaxfev})
            assert result["nfev"] == imaxfev

