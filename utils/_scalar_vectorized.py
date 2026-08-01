
def _scalar_vectorized(scalar, M):
    """
    Scalar product between scalars and matrices.
    """
    return scalar[:, np.newaxis, np.newaxis]*M

