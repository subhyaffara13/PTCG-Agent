
def test_bug_11886():
    def opt(x):
        return x[0]**2+x[1]**2

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", PendingDeprecationWarning)
        A = np.matrix(np.diag([1, 1]))
    lin_cons = LinearConstraint(A, -1, np.inf)
    # just checking that there are no errors
    minimize(opt, 2*[1], constraints = lin_cons)

