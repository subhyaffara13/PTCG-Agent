
def _make_log_data():
    """Data spanning 1 to ~1000 for log scale."""
    t = np.linspace(0, 2 * np.pi, 50)
    x = 10 ** (t / 2)
    y = 10 ** (1 + np.sin(t))
    z = 10 ** (2 * (1 + np.cos(t) / 2))
    return x, y, z

