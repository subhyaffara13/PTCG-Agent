
def _tau_b(A):
    """Calculate Kendall's tau-b and p-value from contingency table."""
    # See [2] 2.2 and 4.2

    # contingency table must be truly 2D
    if A.shape[0] == 1 or A.shape[1] == 1:
        return np.nan, np.nan

    NA = A.sum()
    PA = _P(A)
    QA = _Q(A)
    Sri2 = (A.sum(axis=1)**2).sum()
    Scj2 = (A.sum(axis=0)**2).sum()
    denominator = (NA**2 - Sri2)*(NA**2 - Scj2)

    tau = (PA-QA)/(denominator)**0.5

    numerator = 4*(_a_ij_Aij_Dij2(A) - (PA - QA)**2 / NA)
    s02_tau_b = numerator/denominator
    if s02_tau_b == 0:  # Avoid divide by zero
        return tau, 0
    Z = tau/s02_tau_b**0.5
    p = 2*norm.sf(abs(Z))  # 2-sided p-value

    return tau, p

