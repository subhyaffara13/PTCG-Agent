
def _azimuth2math(azimuth, elevation):
    """
    Convert from clockwise-from-north and up-from-horizontal to mathematical
    conventions.
    """
    theta = np.radians((90 - azimuth) % 360)
    phi = np.radians(90 - elevation)
    return theta, phi

