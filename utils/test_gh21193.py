
def test_gh21193():
    # Test that nested minimization does not share Hessian objects
    def identity(x):
        return x[0]
    def identity_jac(x):
        a = np.zeros(len(x))
        a[0] = 1
        return a
    constraint1 = NonlinearConstraint(identity, 0, 0, identity_jac)
    constraint2 = NonlinearConstraint(identity, 0, 0, identity_jac)

    # The default HUS for each should be distinct
    assert constraint1.hess is not constraint2.hess

    _ = minimize(
        lambda x: minimize(
            rosen,
            x[1:],
            jac=rosen_der,
            constraints=constraint1,
            method="trust-constr",
            options={'maxiter': 2},
        ).fun,
        [1, 0, 0],
        constraints=constraint2,
        method="trust-constr",
        options={'maxiter': 2},
    )

