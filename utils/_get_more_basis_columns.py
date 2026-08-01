
def _get_more_basis_columns(A, basis):
    """
    Called when the auxiliary problem terminates with artificial columns in
    the basis, which must be removed and replaced with non-artificial
    columns. Finds additional columns that do not make the matrix singular.
    """
    m, n = A.shape

    # options for inclusion are those that aren't already in the basis
    a = np.arange(m+n)
    bl = np.zeros(len(a), dtype=bool)
    bl[basis] = 1
    options = a[~bl]
    options = options[options < n]  # and they have to be non-artificial

    # form basis matrix
    B = np.zeros((m, m))
    B[:, 0:len(basis)] = A[:, basis]

    if (basis.size > 0 and
            np.linalg.matrix_rank(B[:, :len(basis)]) < len(basis)):
        raise Exception("Basis has dependent columns")

    rank = 0  # just enter the loop
    for i in range(n):  # somewhat arbitrary, but we need another way out
        # permute the options, and take as many as needed
        new_basis = np.random.permutation(options)[:m-len(basis)]
        B[:, len(basis):] = A[:, new_basis]  # update the basis matrix
        rank = np.linalg.matrix_rank(B)      # check the rank
        if rank == m:
            break

    return np.concatenate((basis, new_basis))

