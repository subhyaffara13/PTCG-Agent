
def generate_matrix(N, complex_=False, hermitian=False,
                    pos_definite=False, sparse=False, rng=None):
    M = rng.random((N, N))
    if complex_:
        M = M + 1j * rng.random((N, N))

    if hermitian:
        if pos_definite:
            if sparse:
                i = np.arange(N)
                j = rng.randint(N, size=N-2)
                i, j = np.meshgrid(i, j)
                M[i, j] = 0
            M = np.dot(M.conj(), M.T)
        else:
            M = np.dot(M.conj(), M.T)
            if sparse:
                i = rng.randint(N, size=N * N // 4)
                j = rng.randint(N, size=N * N // 4)
                ind = np.nonzero(i == j)
                j[ind] = (j[ind] + 1) % N
                M[i, j] = 0
                M[j, i] = 0
    else:
        if sparse:
            i = rng.randint(N, size=N * N // 2)
            j = rng.randint(N, size=N * N // 2)
            M[i, j] = 0
    return M

