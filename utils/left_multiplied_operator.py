
def left_multiplied_operator(J, d):
    """Return diag(d) J as LinearOperator."""
    J = aslinearoperator(J)

    def matvec(x):
        return d * J.matvec(x)

    def matmat(X):
        return d[:, np.newaxis] * J.matmat(X)

    def rmatvec(x):
        return J.rmatvec(x.ravel() * d)

    return LinearOperator(J.shape, matvec=matvec, matmat=matmat,
                          rmatvec=rmatvec)

