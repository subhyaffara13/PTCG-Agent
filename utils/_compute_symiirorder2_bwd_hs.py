
def _compute_symiirorder2_bwd_hs(k, cs, rsq, omega):
    cssq = cs * cs
    k = np.abs(k)
    rsupk = np.power(rsq, k / 2.0)

    c0 = (cssq * (1.0 + rsq) / (1.0 - rsq) /
          (1 - 2 * rsq * np.cos(2 * omega) + rsq * rsq))
    gamma = (1.0 - rsq) / (1.0 + rsq) / np.tan(omega)
    return c0 * rsupk * (np.cos(omega * k) + gamma * np.sin(omega * k))

