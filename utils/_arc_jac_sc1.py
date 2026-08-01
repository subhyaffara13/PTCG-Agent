
def _arc_jac_sc1(w, m):
    """Real inverse Jacobian sc, with complementary modulus

    Solve for z in w = sc(z, 1-m)

    w - real scalar

    m - modulus

    From [1], sc(z, m) = -i * sn(i * z, 1 - m)

    References
    ----------
    # noqa: E501
    .. [1] https://functions.wolfram.com/EllipticFunctions/JacobiSC/introductions/JacobiPQs/ShowAll.html,
       "Representations through other Jacobi functions"

    """

    zcomplex = _arc_jac_sn(1j * w, m)
    if abs(zcomplex.real) > 1e-14:
        raise ValueError

    return zcomplex.imag

