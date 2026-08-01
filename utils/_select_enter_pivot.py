
def _select_enter_pivot(c_hat, bl, a, rule="bland", tol=1e-12):
    """
    Selects a pivot to enter the basis. Currently Bland's rule - the smallest
    index that has a negative reduced cost - is the default.
    """
    if rule.lower() == "mrc":  # index with minimum reduced cost
        return a[~bl][np.argmin(c_hat)]
    else:  # smallest index w/ negative reduced cost
        return a[~bl][c_hat < -tol][0]

