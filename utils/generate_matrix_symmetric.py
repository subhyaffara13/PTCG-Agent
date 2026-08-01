
def generate_matrix_symmetric(N, pos_definite=False, sparse=False, rng=None):
    M = rng.random((N, N))

    M = 0.5 * (M + M.T)  # Make M symmetric

    if pos_definite:
        Id = N * np.eye(N)
        if sparse:
            M = csr_array(M)
        M += Id
    else:
        if sparse:
            M = csr_array(M)

    return M

