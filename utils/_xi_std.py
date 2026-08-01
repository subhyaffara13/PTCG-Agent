
def _xi_std(r, l, y_continuous, xp):
    # Compute asymptotic standard deviation of xi under null hypothesis of independence

    # `axis=-1` is guaranteed by _axis_nan_policy decorator
    n = r.shape[-1]

    # "Suppose that X and Y are independent and Y is continuous. Then
    # √n·ξn(X, Y) → N(0, 2/5) in distribution as n → ∞"
    if y_continuous:  # [1] Theorem 2.1
        return xp.asarray(math.sqrt(2 / 5) / math.sqrt(n), dtype=r.dtype)

    # "Suppose that X and Y are independent. Then √n·ξn(X, Y)
    # converges to N(0, τ²) in distribution as n → ∞
    # [1] Eq. 2.2 and surrounding math
    i = xp.arange(1, n + 1, dtype=r.dtype)
    u = xp.sort(r, axis=-1)
    v = xp.cumulative_sum(u, axis=-1)
    an = 1 / n**4 * xp.sum((2*n - 2*i + 1) * u**2, axis=-1)
    bn = 1 / n**5 * xp.sum((v + (n - i)*u)**2, axis=-1)
    cn = 1 / n**3 * xp.sum((2*n - 2*i + 1) * u, axis=-1)
    dn = 1 / n**3 * xp.sum((l * (n - l)), axis=-1)
    tau2 = (an - 2*bn + cn**2) / dn**2

    return xp.sqrt(tau2) / math.sqrt(n)

