
def _make_triangulation_data():
    """Data for trisurf with positive values."""
    np.random.seed(42)
    x = np.random.uniform(1, 100, 100)
    y = np.random.uniform(1, 100, 100)
    z = x * y / 10
    return x, y, z

