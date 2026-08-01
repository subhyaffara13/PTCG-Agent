
def moment_mp(m, k, nu):
    """Implementation of the studentized range moment"""
    m, k, nu = mpf(m), mpf(k), mpf(nu)

    def inner(q, s, z):
        return phi(z + q * s) * phi(z) * (Phi(z + q * s) - Phi(z)) ** (k - 2)

    def outer(q, s, z):
        return s ** nu * phi(sqrt(nu) * s) * inner(q, s, z)

    def pdf(q, s, z):
        return (sqrt(2 * pi) * k * (k - 1) * nu ** (nu / 2)
                / (gamma(nu / 2) * 2 ** (nu / 2 - 1)) * outer(q, s, z))

    def whole(q, s, z):
        return q ** m * pdf(q, s, z)

    res = quad(whole, [0, inf], [0, inf], [-inf, inf],
               method="gauss-legendre", maxdegree=10)
    return res

