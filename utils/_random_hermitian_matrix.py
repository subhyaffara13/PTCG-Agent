
def _random_hermitian_matrix(n, posdef=False, dtype=float):
    "Generate random sym/hermitian array of the given size n"
    # FIXME non-deterministic rng
    if dtype in COMPLEX_DTYPES:
        A = np.random.rand(n, n) + np.random.rand(n, n)*1.0j
        A = (A + A.conj().T)/2
    else:
        A = np.random.rand(n, n)
        A = (A + A.T)/2

    if posdef:
        A += sqrt(2*n)*np.eye(n)

    return A.astype(dtype)

