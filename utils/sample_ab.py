
def sample_AB(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """AB matrix.

    AB: rows of B into A. Shape (d, d, n).

    - Copy A into d "pages"
    - In the first page, replace 1st rows of A with 1st row of B.
    ...
    - In the dth page, replace dth row of A with dth row of B.
    - return the stack of pages

    """
    d, n = A.shape
    AB = np.tile(A, (d, 1, 1))
    i = np.arange(d)
    AB[i, i] = B[i]
    return AB

