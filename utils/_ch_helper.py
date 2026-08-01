
def _ch_helper(gamma, s, r, h, p0, p1, x):
    """Helper function for generating picklable cubehelix colormaps."""
    # Apply gamma factor to emphasise low or high intensity values
    xg = x ** gamma
    # Calculate amplitude and angle of deviation from the black to white
    # diagonal in the plane of constant perceived intensity.
    a = h * xg * (1 - xg) / 2
    phi = 2 * np.pi * (s / 3 + r * x)
    return xg + a * (p0 * np.cos(phi) + p1 * np.sin(phi))

