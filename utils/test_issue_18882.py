
def test_issue_18882():
    def lsf(u):
        u1, u2 = u
        a, b = [3.0, 4.0]
        return 1.0 + u1**2 / a**2 - u2**2 / b**2

    def of(u):
        return np.sum(u**2)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "delta_grad == 0.0", UserWarning)
        warnings.filterwarnings("ignore", "Singular Jacobian matrix.", UserWarning)
        res = minimize(
            of,
            [0.0, 0.0],
            method="trust-constr",
            constraints=NonlinearConstraint(lsf, 0, 0),
        )
    assert (not res.success) and (res.constr_violation > 1e-8)

