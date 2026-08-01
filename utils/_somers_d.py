
def _somers_d(A, alternative='two-sided'):
    """Calculate Somers' D and p-value from contingency table."""
    # See [3] page 1740

    # contingency table must be truly 2D
    if A.shape[0] <= 1 or A.shape[1] <= 1:
        return np.nan, np.nan

    NA = A.sum()
    NA2 = NA**2
    PA = _P(A)
    QA = _Q(A)
    Sri2 = (A.sum(axis=1)**2).sum()

    d = (PA - QA)/(NA2 - Sri2)

    S = _a_ij_Aij_Dij2(A) - (PA-QA)**2/NA

    with np.errstate(divide='ignore'):
        Z = (PA - QA)/(4*(S))**0.5

    norm = _stats_py._SimpleNormal()
    p = _stats_py._get_pvalue(Z, norm, alternative, xp=np)

    return d, p

