
def _vandermonde(x, degree, xp=np):
    # Returns a matrix of monomials that span polynomials with the specified
    # degree evaluated at x.
    backend = _get_backend(xp)
    powers = backend._monomial_powers(x.shape[1], degree, xp)
    return backend.polynomial_matrix(x, powers, xp)

