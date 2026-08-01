
def compute_alpha(n):
    """alpha_n from DLMF 8.12.13"""
    coeffs = mp.taylor(eta, 0, n - 1)
    return lagrange_inversion(coeffs)

