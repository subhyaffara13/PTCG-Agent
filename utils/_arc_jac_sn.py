
def _arc_jac_sn(w, m):
    """Inverse Jacobian elliptic sn

    Solve for z in w = sn(z, m)

    Parameters
    ----------
    w : complex scalar
        argument

    m : scalar
        modulus; in interval [0, 1]


    See [1], Eq. (56)

    References
    ----------
    .. [1] Orfanidis, "Lecture Notes on Elliptic Filter Design",
           https://www.ece.rutgers.edu/~orfanidi/ece521/notes.pdf

    """

    def _complement(kx):
        # (1-k**2) ** 0.5; the expression below
        # works for small kx
        return ((1 - kx) * (1 + kx)) ** 0.5

    k = m ** 0.5

    if k > 1:
        return np.nan
    elif k == 1:
        return np.arctanh(w)

    ks = [k]
    niter = 0
    while ks[-1] != 0:
        k_ = ks[-1]
        k_p = _complement(k_)
        ks.append((1 - k_p) / (1 + k_p))
        niter += 1
        if niter > _ARC_JAC_SN_MAXITER:
            raise ValueError('Landen transformation not converging')

    K = np.prod(1 + np.array(ks[1:])) * np.pi/2

    wns = [w]

    for kn, knext in zip(ks[:-1], ks[1:]):
        wn = wns[-1]
        wnext = (2 * wn /
                 ((1 + knext) * (1 + _complement(kn * wn))))
        wns.append(wnext)

    u = 2 / np.pi * np.arcsin(wns[-1])

    z = K * u
    return z

