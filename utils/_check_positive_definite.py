
def _check_positive_definite(Hk):
    def is_pos_def(A):
        if issymmetric(A):
            try:
                cholesky(A)
                return True
            except LinAlgError:
                return False
        else:
            return False
    if Hk is not None:
        if not is_pos_def(Hk):
            raise ValueError("'hess_inv0' matrix isn't positive definite.")

