
def _matrix_vector_product_of_stacks(A, b):
    """Compute the product of stack of matrices and vectors."""
    return np.einsum("ijk,ik->ij", A, b)

