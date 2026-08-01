
def _make_surface_log_data():
    """Grid data for surface with positive Z."""
    x = np.linspace(1, 10, 20)
    y = np.linspace(1, 10, 20)
    X, Y = np.meshgrid(x, y)
    Z = X * Y
    return X, Y, Z

