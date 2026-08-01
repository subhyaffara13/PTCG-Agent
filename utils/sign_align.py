
def sign_align(A, B):
    """Align signs of columns of A match those of B: column-wise remove
    sign of A by multiplying with its sign then multiply in sign of B.
    """
    return np.array([col_A * np.sign(col_A[0]) * np.sign(col_B[0])
                     for col_A, col_B in zip(A.T, B.T)]).T

