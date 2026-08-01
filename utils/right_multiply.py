
def right_multiply(J, d, copy=True):
    """Compute J diag(d).

    If `copy` is False, `J` is modified in place (unless being LinearOperator).
    """
    if copy and not isinstance(J, LinearOperator):
        J = J.copy()

    if issparse(J):
        J.data *= d.take(J.indices, mode='clip')  # scikit-learn recipe.
    elif isinstance(J, LinearOperator):
        J = right_multiplied_operator(J, d)
    else:
        J *= d

    return J

