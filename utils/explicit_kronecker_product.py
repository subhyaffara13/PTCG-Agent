
def explicit_kronecker_product(kron):
    # Make sure we have a sequence of Matrices
    if not all(isinstance(m, MatrixBase) for m in kron.args):
        return kron

    return matrix_kronecker_product(*kron.args)

