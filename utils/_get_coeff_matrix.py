import math


def _get_coeff_matrix(n):
    """
    Compute the matrix for converting Bezier control points to polynomial
    coefficients for a curve of degree n.

    The matrix M is such that M @ control_points gives polynomial coefficients.
    Entry M[j, i] = C(n, j) * (-1)^(i+j) * C(j, i) where C is the binomial
    coefficient.
    """
    def _comb(n, k):
        return np.vectorize(math.comb)(n, k)

    j = np.arange(n + 1)[:, None]
    i = np.arange(n + 1)[None, :]  # _comb is non-zero for i <= j
    prefactor = (-1) ** (i + j) * _comb(j, i)  # j on axis 0, i on axis 1
    return (_comb(n, j) * prefactor).astype(float)

