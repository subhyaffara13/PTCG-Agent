
def test_gh_18793_and_19351():
    answer = 1e-12
    initial_guess = 1.1e-12

    def chi2(x):
        return (x-answer)**2

    gtol = 1e-15
    res = least_squares(chi2, x0=initial_guess, gtol=1e-15, bounds=(0, np.inf))
    # Original motivation: gh-18793
    # if we choose an initial condition that is close to the solution
    # we shouldn't return an answer that is further away from the solution

    # Update: gh-19351
    # However this requirement does not go well with 'trf' algorithm logic.
    # Some regressions were reported after the presumed fix.
    # The returned solution is good as long as it satisfies the convergence
    # conditions.
    # Specifically in this case the scaled gradient will be sufficiently low.

    scaling, _ = CL_scaling_vector(res.x, res.grad,
                                   np.atleast_1d(0), np.atleast_1d(np.inf))
    assert res.status == 1  # Converged by gradient
    assert np.linalg.norm(res.grad * scaling, ord=np.inf) < gtol

