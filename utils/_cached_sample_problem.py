
def _cached_sample_problem(make_complex: bool):
    # A random 10 x 10 symmetric matrix
    rng = np.random.RandomState(1234)
    if make_complex:
        matrix = rng.rand(10, 10) + 1j * rng.rand(10, 10)
        matrix = matrix + matrix.T.conj()
    else:
        matrix = rng.rand(10, 10)
        matrix = matrix + matrix.T
    # A random vector of length 10
    vector = rng.rand(10)
    return matrix, vector

