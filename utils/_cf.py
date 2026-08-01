
def _cf(Phi, t, alpha, beta):
    """Characteristic function."""
    return np.exp(
        -(np.abs(t) ** alpha) * (1 - 1j * beta * np.sign(t) * Phi(alpha, t))
    )

