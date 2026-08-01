
def _create_block_3_diagonal_matrix(A, B, d):
    """Create a 3-diagonal block matrix as banded.

    The matrix has the following structure:

        DB...
        ADB..
        .ADB.
        ..ADB
        ...AD

    The blocks A, B and D are 3-by-3 matrices. The D matrices has the form
    d * I.

    Parameters
    ----------
    A : ndarray, shape (n, 3, 3)
        Stack of A blocks.
    B : ndarray, shape (n, 3, 3)
        Stack of B blocks.
    d : ndarray, shape (n + 1,)
        Values for diagonal blocks.

    Returns
    -------
    ndarray, shape (11, 3 * (n + 1))
        Matrix in the banded form as used by `scipy.linalg.solve_banded`.
    """
    ind = np.arange(3)
    ind_blocks = np.arange(len(A))

    A_i = np.empty_like(A, dtype=int)
    A_i[:] = ind[:, None]
    A_i += 3 * (1 + ind_blocks[:, None, None])

    A_j = np.empty_like(A, dtype=int)
    A_j[:] = ind
    A_j += 3 * ind_blocks[:, None, None]

    B_i = np.empty_like(B, dtype=int)
    B_i[:] = ind[:, None]
    B_i += 3 * ind_blocks[:, None, None]

    B_j = np.empty_like(B, dtype=int)
    B_j[:] = ind
    B_j += 3 * (1 + ind_blocks[:, None, None])

    diag_i = diag_j = np.arange(3 * len(d))
    i = np.hstack((A_i.ravel(), B_i.ravel(), diag_i))
    j = np.hstack((A_j.ravel(), B_j.ravel(), diag_j))
    values = np.hstack((A.ravel(), B.ravel(), np.repeat(d, 3)))

    u = 5
    l = 5
    result = np.zeros((u + l + 1, 3 * len(d)))
    result[u + i - j, j] = values
    return result

