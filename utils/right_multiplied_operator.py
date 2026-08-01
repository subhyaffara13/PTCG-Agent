
def right_multiplied_operator(J, d):
    """Return J diag(d) as LinearOperator."""
    J = aslinearoperator(J)

    def matvec(x):
        return J.matvec(np.ravel(x) * d)

    def matmat(X):
        return J.matmat(X * d[:, np.newaxis])

    def rmatvec(x):
        return d * J.rmatvec(x)

    return LinearOperator(J.shape, matvec=matvec, matmat=matmat,
                          rmatvec=rmatvec)

