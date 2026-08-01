
def _ellipdeg(n, m1):
    """Solve degree equation using nomes

    Given n, m1, solve
       n * K(m) / K'(m) = K1(m1) / K1'(m1)
    for m

    See [1], Eq. (49)

    References
    ----------
    .. [1] Orfanidis, "Lecture Notes on Elliptic Filter Design",
           https://www.ece.rutgers.edu/~orfanidi/ece521/notes.pdf
    """
    K1 = special.ellipk(m1)
    K1p = special.ellipkm1(m1)

    q1 = np.exp(-np.pi * K1p / K1)
    q = q1 ** (1/n)

    mnum = np.arange(_ELLIPDEG_MMAX + 1)
    mden = np.arange(1, _ELLIPDEG_MMAX + 2)

    num = np.sum(q ** (mnum * (mnum+1)))
    den = 1 + 2 * np.sum(q ** (mden**2))

    return 16 * q * (num / den) ** 4

