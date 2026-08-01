
def random_entry(n, min_eig, max_eig, case, rng=None):
    rng = np.random.default_rng(rng)

    # Generate random matrix
    rand = rng.uniform(low=-1, high=1, size=(n, n))

    # QR decomposition
    Q, _, _ = qr(rand, pivoting='True')

    # Generate random eigenvalues
    eigvalues = rng.uniform(low=min_eig, high=max_eig, size=n)
    eigvalues = np.sort(eigvalues)[::-1]

    # Generate matrix
    Qaux = np.multiply(eigvalues, Q)
    A = np.dot(Qaux, Q.T)

    # Generate gradient vector accordingly
    # to the case is being tested.
    if case == 'hard':
        g = np.zeros(n)
        g[:-1] = rng.uniform(low=-1, high=1, size=n-1)
        g = np.dot(Q, g)
    elif case == 'jac_equal_zero':
        g = np.zeros(n)
    else:
        g = rng.uniform(low=-1, high=1, size=n)

    return A, g

