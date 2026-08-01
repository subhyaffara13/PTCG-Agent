
def pdf_mp(q, k, nu):
    """Straightforward implementation of studentized range PDF"""
    q, k, nu = mpf(q), mpf(k), mpf(nu)

    def inner(s, z):
        return phi(z + q * s) * phi(z) * (Phi(z + q * s) - Phi(z)) ** (k - 2)

    def outer(s, z):
        return s ** nu * phi(sqrt(nu) * s) * inner(s, z)

    def whole(s, z):
        return (sqrt(2 * pi) * k * (k - 1) * nu ** (nu / 2)
                / (gamma(nu / 2) * 2 ** (nu / 2 - 1)) * outer(s, z))

    res = quad(whole, [0, inf], [-inf, inf],
               method="gauss-legendre", maxdegree=10)
    return res

