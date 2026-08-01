
def _sum_basis_elements(x, t, c, k):
    n = len(t) - (k+1)
    assert n >= k+1
    assert c.shape[0] >= n
    s = 0.
    for i in range(n):
        b = BSpline.basis_element(t[i:i+k+2], extrapolate=False)(x)
        s += c[i] * np.nan_to_num(b)   # zero out out-of-bounds elements
    return s

