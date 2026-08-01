
def lpgen_2d(m, n):
    """ -> A b c LP test: m*n vars, m+n constraints
        row sums == n/m, col sums == 1
        https://gist.github.com/denis-bz/8647461
    """
    rng = np.random.default_rng(35892345982340246935)
    c = - rng.exponential(size=(m, n))
    Arow = np.zeros((m, m * n))
    brow = np.zeros(m)
    for j in range(m):
        j1 = j + 1
        Arow[j, j * n:j1 * n] = 1
        brow[j] = n / m

    Acol = np.zeros((n, m * n))
    bcol = np.zeros(n)
    for j in range(n):
        j1 = j + 1
        Acol[j, j::n] = 1
        bcol[j] = 1

    A = np.vstack((Arow, Acol))
    b = np.hstack((brow, bcol))

    return A, b, c.ravel()

