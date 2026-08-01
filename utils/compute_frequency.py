
def compute_frequency(t, theta):
    """
    Compute theta'(t)/(2*pi), where theta'(t) is the derivative of theta(t).
    """
    # Assume theta and t are 1-D NumPy arrays.
    # Assume that t is uniformly spaced.
    dt = t[1] - t[0]
    f = np.diff(theta)/(2*np.pi) / dt
    tf = 0.5*(t[1:] + t[:-1])
    return tf, f

