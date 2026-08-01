
def _symeig_backward(D_grad, U_grad, A, D, U, largest):
    # if `U` is square, then the columns of `U` is a complete eigenspace
    if U.size(-1) == U.size(-2):
        return _symeig_backward_complete_eigenspace(D_grad, U_grad, A, D, U)
    else:
        return _symeig_backward_partial_eigenspace(D_grad, U_grad, A, D, U, largest)

