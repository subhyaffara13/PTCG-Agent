
def _quadratic_roots_in_01(c0, c1, c2):
    """Real roots of c0 + c1*x + c2*x**2 in [0, 1]."""
    if abs(c2) < 1e-12:  # Linear
        if abs(c1) < 1e-12:
            return np.array([])
        root = -c0 / c1
        return np.array([root]) if 0 <= root <= 1 else np.array([])

    disc = c1 * c1 - 4 * c2 * c0
    if disc < 0:
        return np.array([])

    sqrt_disc = np.sqrt(disc)
    # Numerically stable quadratic formula
    if c1 >= 0:
        q = -0.5 * (c1 + sqrt_disc)
    else:
        q = -0.5 * (c1 - sqrt_disc)

    roots = []
    if abs(q) > 1e-12:
        roots.append(c0 / q)
    if abs(c2) > 1e-12:
        roots.append(q / c2)

    roots = np.asarray(roots)
    return roots[(roots >= 0) & (roots <= 1)]

