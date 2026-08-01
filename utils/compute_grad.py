
def compute_grad(J, f):
    """Compute gradient of the least-squares cost function."""
    if isinstance(J, LinearOperator):
        return J.rmatvec(f)
    else:
        return J.T.dot(f)

